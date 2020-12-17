# -*- coding: utf-8 -*-
"""
Main application:

USER
/ - index
/search - formula search
/formula/<int:formula_id> - single formula page

API
/api/formula_search - search API
"""
from flask import Flask, render_template, request, jsonify
from models import db
from search import Search


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ice_site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db.app = app
db.init_app(app)
db.create_all()

search = Search()


@app.route('/')
def index():
    """Index page"""
    return render_template("index.html")


@app.route('/search')
def search_page():
    """Search page"""
    return render_template("search.html")


@app.route("/api/formula_search", methods=["GET", "POST"])
def api_search():
    """API: list of formulas"""
    data = search.formula_search(request)
    return jsonify(data)


@app.route("/formula/<int:formula_id>")
def formula_view(formula_id):
    """Page for single formula"""
    data = search.get_formula_contexts(formula_id)
    return render_template("formula.html", data=data)


if __name__ == '__main__':
    app.run(debug=True)
