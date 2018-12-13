#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os.path
import sys
import traceback

import platform
import signal
import functools
from functools import partial

import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import flask
import flask_login

from flask import url_for, request, session, redirect
from flask import Flask, render_template
from flask_babel import Babel
from babel.support import Translations
from flask_bower import Bower

from tornado.options import define, options
from tornado.wsgi import WSGIContainer
from tornado.web import FallbackHandler

APP_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(APP_DIR)

import app.settings as settings
import app.controllers.main
import app.controllers.dataset
import app.domain.dataset
import app.data_tables.ajax_adapter

DEBUG = False
DATASETS_PATH = os.path.join(APP_DIR, 'datasets')

class Application(tornado.web.Application):
    """Application object."""

    def __init__(self):
        template_path = os.path.join(APP_DIR, "app/templates")
        static_path = os.path.join(APP_DIR, "app/static")
        flask_app = Flask(__name__, static_folder=static_path, template_folder=template_path)
        self.__flask_app = flask_app
        flask_app.secret_key = "\x81\xb6\xcc\xbdep\xff\\\xfbu\xec~R\xb8S\x12\xddm0\x0e\xdc\xdc\x07\xee"
        babel = Babel(flask_app)
        Bower(flask_app)

        flask_app.before_request(self.__before_request)
        flask_app.context_processor(self.__inject_locale_info)

        self.__login_manager = flask_login.LoginManager()
        self.__login_manager.init_app(flask_app)

        main_controller = app.controllers.main.MainController(self.__get_locale)
        flask_app.add_url_rule('/', view_func=main_controller.root)
        flask_app.add_url_rule('/<locale>', view_func=main_controller.index)
        flask_app.add_url_rule('/datasets/', view_func=main_controller.datasets)
        # self.add_url_rule('/datasets/', fget=main_controller.datasets)
        # flask_app.add_url_rule('/kernels/', view_func=main_controller.kernels)
        self.add_url_rule('/kernels/', fget=main_controller.kernels)

        ds_factory = app.domain.dataset.DatasetFactory()
        ds_mapper = app.domain.dataset.DatasetMapper(DATASETS_PATH, ds_factory)
        ds_controller = app.controllers.dataset.DatasetController(ds_mapper, DATASETS_PATH)
        self.add_url_rule('/datasets/list/', fget=ds_controller.list)
        flask_app.add_url_rule('/storage/<path:ds_path>/', view_func=ds_controller.upload, methods=['POST'])

        flask_app.config['DEBUG'] = DEBUG
        flask_app.config['BABEL_DEFAULT_LOCALE'] = settings.DEFAULT_LOCALE
        flask_app.config['BOWER_COMPONENTS_ROOT'] = 'app/static/bower_components'
        flask_app.config['MAX_CONTENT_LENGTH'] = settings.MAX_CONTENT_LENGTH

        wsgi_container = WSGIContainer(flask_app)

        # tornado settings
        handlers = [
            (r".*", FallbackHandler, dict(fallback=wsgi_container)),
        ]
        s = dict(xsrf_cookies=False, cookie_secret="11oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=", debug=DEBUG)
        tornado.web.Application.__init__(self, handlers, **s)

    # def add_url_rule(self, rule, allowed_for, **kwargs):
    def add_url_rule(self, rule, **kwargs):
        view = app.data_tables.ajax_adapter.AjaxAdapter.as_view(rule, **kwargs)
        # view = self.__update_session(view)
        # view = allowed_for(view)
        self.__flask_app.add_url_rule(rule, view_func=view)

    @staticmethod
    def __update_session(f):
        @functools.wraps(f)
        def wrapped_f(*args, **kwargs):
            flask_login.current_user.update_session()
            return f(*args, **kwargs)
        return wrapped_f

    # to avoid the locale parameter in every request handler
    @staticmethod
    def __before_request():
        if flask.request.view_args and 'locale' in flask.request.view_args:
            locale = flask.request.view_args['locale']
            if locale in settings.LOCALES:
                flask.session["locale"] = locale
            flask.request.view_args.pop('locale')


    @staticmethod
    def __inject_locale_info():
        vars = dict()
        vars['locale_selector_state'] = Application.__locale_selector_state()
        vars['locale'] = Application.__get_locale()
        vars['datatables_locale'] = 'datatables/i18n/en_US.json'
        return vars


    @staticmethod
    def __locale_selector_state():
        current_locale = Application.__get_locale()

        def active_locale_class(locale):
            return "active" if locale == current_locale else ""

        state = {
            settings.EN_LOCALE: active_locale_class(settings.EN_LOCALE),
            settings.DE_LOCALE: active_locale_class(settings.DE_LOCALE),
            settings.RU_LOCALE: active_locale_class(settings.RU_LOCALE),
        }

        return state

    @staticmethod
    def __get_locale():
        locale = flask.session.get('locale')
        if locale is not None:
            return locale

        # otherwise try to guess the language from the user accept
        # header the browser transmits. The best match wins.
        locale = flask.request.accept_languages.best_match(settings.LOCALES)
        if locale is not None:
            return locale

        return settings.DEFAULT_LOCALE


def main():
    """App entry point"""

    define("address", default="127.0.0.1", help="Run on the given ip")
    define("port", default=8080, help="Run on the given port", type=int)

    tornado.options.parse_command_line()

    def signal_handler(signum, frame):
        print("Signal received {}".format(signum))
        if signum in (signal.SIGINT, signal.SIGTERM):
            print("Exiting...")
            exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    if platform.system() == 'Windows':
        signal.signal(signal.SIGBREAK, signal_handler)

    app = Application()
    app.listen(options.port, options.address)

    print('Starting forever loop...')
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exception(*sys.exc_info())
        print("An error encountered: " + str(e))

