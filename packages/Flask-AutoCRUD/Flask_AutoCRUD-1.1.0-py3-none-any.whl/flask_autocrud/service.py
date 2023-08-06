from flask import abort
from flask import request

from sqlalchemy import asc
from sqlalchemy import desc
from flask.views import MethodView

from .wrapper import get_json
from .wrapper import resp_csv
from .wrapper import resp_json
from .wrapper import no_content
from .wrapper import response_with_links
from .wrapper import response_with_location


class Service(MethodView):
    __db__ = None
    __model__ = None
    __collection_name__ = 'resources'

    def delete(self, resource_id):
        """

        :param resource_id:
        :return:
        """
        model = self.__model__
        session = self.__db__.session()

        resource = model.query.get(resource_id)
        if not resource:
            abort(resp_json({'message': 'Not Found'}, code=404))

        session.delete(resource)
        session.commit()
        return no_content()

    def get(self, resource_id=None):
        """

        :param resource_id:
        :return:
        """
        model = self.__model__

        if resource_id is None:
            if request.path.endswith('meta'):
                return resp_json(model.description())

            response = resp_csv if 'export' in request.args else resp_json
            return response(self._all_resources(), self.__collection_name__)
        else:
            resource = model.query.get(resource_id)
            if not resource:
                abort(resp_json({'message': 'Not Found'}, code=404))
            return response_with_links(resource)

    def patch(self, resource_id):
        """

        :param resource_id:
        :return:
        """
        model = self.__model__
        session = self.__db__.session()

        data = get_json()
        self._validate_fields(data)

        resource = model.query.get(resource_id)
        if not resource:
            abort(resp_json({'message': 'Not Found'}, code=404))

        resource.update(data)
        session.merge(resource)
        session.commit()

        return response_with_links(resource)

    def post(self):
        """

        :return:
        """
        model = self.__model__
        session = self.__db__.session()

        data = get_json()
        self._validate_fields(data)

        resource = model.query.filter_by(**data).first()
        if not resource:
            resource = model(**data)
            session.add(resource)
            session.commit()
            code = 201
        else:
            code = 409

        return response_with_location(resource, code)

    def put(self, resource_id):
        """

        :param resource_id:
        :return:
        """
        model = self.__model__
        session = self.__db__.session()

        data = get_json()
        self._validate_fields(data)

        resource = model.query.get(resource_id)
        if resource:
            resource.update(data)
            session.merge(resource)
            session.commit()

            return response_with_links(resource)

        resource = model(**data)

        session.add(resource)
        session.commit()

        return response_with_links(resource, 201)

    def _all_resources(self):
        """

        :return:
        """
        limit = None
        model = self.__model__
        queryset = model.query

        args = {k: v for (k, v) in request.args.items() if k not in ('page', 'export')}
        if args:
            order = filters = invalid = []

            for k, v in args.items():
                if v.startswith('%'):
                    filters.append(getattr(model, k).like(str(v), escape='/'))
                elif k == 'sort':
                    direction = desc if v.startswith('-') else asc
                    order.append(direction(getattr(model, v.lstrip('-'))))
                elif k == 'limit':
                    limit = int(v)
                elif hasattr(model, k):
                    filters.append(getattr(model, k) == v)
                else:
                    invalid.append(k)

                if len(invalid):
                    abort(resp_json({'invalid': invalid}, code=400))

                queryset = queryset.filter(*filters).order_by(*order)

        if 'page' in request.args:
            resources = queryset.paginate(
                page=int(request.args['page']),
                per_page=limit
            ).items
        else:
            queryset = queryset.limit(limit)
            resources = queryset.all()

        return [r.to_dict() for r in resources]

    def _validate_fields(self, data):
        """

        :param data:
        """
        model = self.__model__
        fields = model.required() + model.optional()
        unknown = [k for k in data if k not in fields]
        missing = set(model.required()) - set(data)

        if len(unknown) or len(missing):
            abort(resp_json({
                'unknown': unknown,
                'missing': list(missing)
            }, code=422))
