# app/views.py
from flask import render_template
from flask.views import View


class Index(View):
    template = "index.html"

    def dispatch_request(self):
        return render_template(self.template)
