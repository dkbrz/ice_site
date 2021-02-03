# -*- coding: utf-8 -*-
"""
Main application:

USER
/ - index
/search - formula search
/formula/<int:formula_id> - single formula page

API
/api_part/formula_search - search API
/api_part/contexts/<formula_id> - contexts for one formula (with span)
"""
from flask import Flask, render_template
from api_part.api import FormulaContexts
from config import API_URL

app = Flask(__name__)


@app.context_processor
def add_prefix():
    """Add prefix (for main_site on host/folklore path)"""
    return dict(prefix=API_URL)


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
    app.run(debug=True, port=5000)
