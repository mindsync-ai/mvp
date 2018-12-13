import json
import pytest
from flask import Flask
from unittest.mock import Mock
from uuid import uuid4

from app.data_tables.ajax_adapter import AjaxAdapter, wrap_single_row_handler
from app.data_tables.field_errors import FieldError, FieldErrors


@pytest.fixture
def app():
    res = Flask(__name__)
    res.testing = True
    return res


def test_adapt_fget(app):
    fget = Mock(return_value=dict(aaa='bbb', ccc=123))
    app.add_url_rule('/get_fruit/<fruit>', view_func=AjaxAdapter.as_view('xxx', fget))
    params = dict(param1='qwerty', param2='12345', _='xxxxxxxxx')
    rv = app.test_client().get('/get_fruit/apple', query_string=params)
    assert rv.status_code == 200
    fget.assert_called_with(fruit='apple', param1='qwerty', param2='12345')
    assert json.loads(rv.data.decode('utf-8')) == fget.return_value


@pytest.mark.parametrize('action', ['create', 'edit', 'remove'])
def test_adapt_post(app, action):
    faction_name = 'f' + action

    faction = Mock(return_value=dict(aaa='bbb', ccc=123))

    form_data = {
        'action': action,
        'foo': 'qwerty',
        'data[id0][aaa]': 'qweqwe',
        'data[id0][bbb]': 'asdasd',
        'data[id1][ccc]': 'dfgdfg',
    }

    rule = '/' + faction_name + '/<fruit>'
    app.add_url_rule(rule, view_func=AjaxAdapter.as_view(faction_name, **{faction_name: faction}))
    rv = app.test_client().post('/' + faction_name + '/apple', data=dict(form_data))
    assert rv.status_code == 200

    expected_args = dict()
    expected_args['fruit'] = 'apple'
    expected_args['foo'] = 'qwerty'
    expected_args['data'] = dict()
    expected_args['data']['id0'] = dict()
    expected_args['data']['id0']['aaa'] = 'qweqwe'
    expected_args['data']['id0']['bbb'] = 'asdasd'
    expected_args['data']['id1'] = dict()
    expected_args['data']['id1']['ccc'] = 'dfgdfg'
    faction.assert_called_with(**expected_args)

    assert json.loads(rv.data.decode('utf-8')) == faction.return_value


FIELD_NAME = 'qweqwe'
FIELD_STATUS = 'sdfsdf'


@pytest.mark.parametrize('action', ['create', 'edit', 'remove'])
@pytest.mark.parametrize('error', [
    FieldError(name=FIELD_NAME, status=FIELD_STATUS),
    FieldErrors({FIELD_NAME: FIELD_STATUS}),
])
def test_adapt_post_should_catch_field_error(app, action, error):
    faction_name = 'f' + action
    faction = Mock(side_effect=error)
    form_data = dict(action=action)
    rule = '/' + str(uuid4())
    app.add_url_rule(rule, view_func=AjaxAdapter.as_view(rule, **{faction_name: faction}))

    rv = app.test_client().post(rule, data=dict(form_data))
    assert rv.status_code == 200
    expected_args = dict()
    faction.assert_called_with(**expected_args)
    assert json.loads(rv.data.decode('utf-8')) == dict(fieldErrors=[dict(name=FIELD_NAME, status=FIELD_STATUS)])


def test_single_row_handler_wrapper():
    handler = Mock(return_value=dict(aaa='bbb', ccc=123))
    wrapped = wrap_single_row_handler(handler)
    multi_row_style_args = dict(fruit='apple', foo='qwerty', data=dict(id0=dict(aaa='qweqwe', bbb='asdasd')))
    assert wrapped(**multi_row_style_args) == handler.return_value
    single_row_style_args = dict(fruit='apple', foo='qwerty', id='id0', aaa='qweqwe', bbb='asdasd')
    handler.assert_called_with(**single_row_style_args)


@pytest.mark.parametrize('bad_args', [dict(data=dict()), dict(data=dict(id0=dict(aaa=111), id1=dict(bbb=222)))])
def test_single_row_handler_wrapper_should_throw_if_bad_row_count(bad_args):
    wrapped = wrap_single_row_handler(Mock())
    with pytest.raises(Exception):
        wrapped(**bad_args)
