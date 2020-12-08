import json
from flask import Flask, render_template, request, jsonify, redirect, url_for
from models import db, ClusterFilters as Cf, NgramEntries as Ne
# from search import db, Search

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ice_site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db.app = app
db.init_app(app)
# db.create_all()

MIN = 0
MAX = 1000


class Search:

    def __init__(self):
        pass

    def formula_search(self, request):
        n_texts_min = request.values.get("n_texts_min", MIN)
        n_texts_max = request.values.get("n_texts_max", MAX)
        n_entries_min = request.values.get("n_entries_min", MIN)
        n_entries_max = request.values.get("n_entries_max", MAX)
        result = Cf.query.filter(
            Cf.n_entries >= n_entries_min,
            Cf.n_entries <= n_entries_max,
            Cf.unique_text >= n_texts_min,
            Cf.unique_text <= n_texts_max
        ).group_by(
            Cf.short_ngram_id
        ).with_entities(
            Cf.short_ngram_id, Cf.text,
            db.func.sum(Cf.n_entries), db.func.count(Cf.n_entries)
        ).order_by(Cf.text).distinct().all()
        return self.formula_to_dict(result)

    @staticmethod
    def formula_to_dict(raw_result):
        result = []
        # print(raw_result)
        for item in raw_result:
            result.append({
                "id": item.short_ngram_id,
                "text": item.text,
                "n_entries": item[2],
                "n_clusters": item[3],
            })
        return result

    def formula_contexts(self, short_ngram_id):
        contexts = Ne.query.filter(Ne.short_ngram_id == short_ngram_id).all()
        print(contexts)
        result = []
        for context in contexts:
            result.append({
                # "text_id": context.text,
                # "chapter_id": context.chapter,
                # "paragraph_idx": context.paragraph,
                # "sentence_idx": context.sentence,
                "cluster_id": context.cluster_id,
                "sentence_unique": context.sentence_unique,
                "text": ""  # self.render_text(context.words)
            })
        return result

    @staticmethod
    def render_text(words):
        result = []
        started, ended = False, False
        for word in words:
            if word.is_formula and not started:
                result += '<span class="f-page-formula">'
                started = True
            elif not word.is_formula and not ended:
                result += '</span>'
            result.append(word.wordform)
        return " ".join(result)


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


@app.route("/group/<int:group_id>")
def cluster_view(group_id):
    data = search.formula_contexts(group_id)
    return render_template("group.html", data=data)


if __name__ == '__main__':
    app.run(debug=True)
