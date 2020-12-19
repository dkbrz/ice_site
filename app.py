# -*- coding: utf-8 -*-
"""
Main application:

USER
/ - index
/search - formula search
/formula/<int:formula_id> - single formula page

API
/api/formula_search - search API
/api/contexts/<formula_id> - contexts for one formula (with span)
"""
from flask import Flask, render_template
from flask_restful import Api
from models import db
from api.api import FormulaSearch, FormulaContexts


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ice_site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db.app = app
db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(FormulaSearch, '/api/formula_search')
api.add_resource(FormulaContexts, '/api/contexts/<formula_id>')


@app.route('/')
def index():
    """Index page"""
    return render_template("index.html")


@app.route('/search')
def search_page():
    """Search page"""
    return render_template("search.html")


@app.route("/formula/<int:formula_id>")
def formula_view(formula_id):
    """Page for single formula"""
    data = FormulaContexts.get(formula_id, as_dict=True)
    return render_template("formula.html", data=data)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == '__main__':
    app.run(debug=True)
