import json
import flask
from flask.views import MethodView
import re

from app.data_tables.field_errors import FieldError, FieldErrors


def _parse_form_data_item_key(key):
    m = re.search('data\[(.*)\]\[(.*)\]', key)
    if m:
        row_id = m.group(1)
        field_name = m.group(2)
        return row_id, field_name
    else:
        return None, None


class AjaxAdapter(MethodView):
    def __init__(self, fget=None, fcreate=None, fedit=None, fremove=None):
        self.__fget = fget
        self.__fcreate = fcreate
        self.__fedit = fedit
        self.__fremove = fremove

    def get(self, **url_variable_parts):
        request_args = dict(flask.request.args.items())
        if '_' in request_args:
            del request_args['_']
        res = self.__fget(**url_variable_parts, **request_args)
        return res if isinstance(res, str) else json.dumps(res)

    def post(self, **url_variable_parts):
        form_data = dict(flask.request.form.items())

        row_data = dict()
        extra_data = dict()
        for form_data_key, form_data_value in form_data.items():
            row_id, property_name = _parse_form_data_item_key(form_data_key)
            if row_id is not None:
                if not row_id in row_data:
                    row_data[row_id] = dict()
                row_data[row_id][property_name] = form_data_value
            else:
                extra_data[form_data_key] = form_data_value

        handler_args = dict()
        handler_args.update(url_variable_parts)
        handler_args.update(extra_data)

        if len(row_data):
            handler_args['data'] = row_data

        action = 'edit'
        if 'action' in handler_args:
            action = handler_args['action']
            del handler_args['action']

        faction = None
        faction = self.__fcreate if action == 'create' else faction
        faction = self.__fedit if action == 'edit' else faction
        faction = self.__fremove if action == 'remove' else faction

        try:
            return json.dumps(faction(**handler_args))
        except FieldError as fe:
            return json.dumps(dict(fieldErrors=[dict(name=fe.name, status=fe.status)]))
        except FieldErrors as fe:
            return json.dumps(dict(fieldErrors=[dict(name=key, status=value) for key, value in fe.to_dict().items()]))


def wrap_single_row_handler(handler):
    def wrapper(data, **other_args):
        row_count = len(data)
        if row_count != 1:
            raise Exception('Single row handler received bad input, len(data)={}'.format(row_count))
        for id, row_props in data.items():
            other_args.update(dict(id=id))
            other_args.update(row_props)
            break
        return handler(**other_args)
    return wrapper
