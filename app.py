import json
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
    return render_template("index.html")


@app.route('/search')
def search_page():
    search_values = {
    }
    return render_template("search.html", data=search_values)


@app.route("/api/formula_search", methods=["GET", "POST"])
def api_search():
    data = search.formula_search(request)
    return jsonify(data)


@app.route("/formula/<formula_id>")
def cluster_view(formula_id):
    data = search.formula_contexts(formula_id)
    return render_template("formula.html", data=data)


if __name__ == '__main__':
    app.run(debug=True)
