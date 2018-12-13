import app.basic
from flask import abort, request, redirect, render_template, url_for, make_response
from werkzeug.exceptions import NotImplemented

class MainController:
    def __init__(self, locale_getter):
        self.__get_locale = locale_getter

    # --------------------------------------------------------------------
    def root(self):
        locale = self.__get_locale()
        return redirect(url_for('index', locale=locale))

    # --------------------------------------------------------------------
    def index(self):
        locale = self.__get_locale()
        return render_template("index.html", locale=locale)

    # ------------------------------------------------------------------------
    def datasets(self):
        return render_template("datasets.html")

    # ------------------------------------------------------------------------
    def kernels(self):
        return render_template("kernels.html")
