# -*- coding: utf-8 -*-
"""
Search module:

1. API for search
2. Entry preprocessing for single-formula page
"""
from flask import jsonify
from flask_restful import Resource, reqparse
from api_part.search import formula_search, get_formula_contexts

parser = reqparse.RequestParser()
parser.add_argument('n_texts_min', type=int)
parser.add_argument('n_texts_max', type=int)
parser.add_argument('n_entries_min', type=int)
parser.add_argument('n_entries_max', type=int)


class FormulaSearch(Resource):
    """
    Formula search API
    INPUT
    n_texts_min, n_texts_max - number of unique texts
    n_entries_min, n_entries_max - number of entries
    OUTPUT
    [
      {
        "id": 1565,
        "n_entries": 4,
        "n_texts": 4,
        "text": "þú hafir hefnt helga",
        "verb_text": "hafa hefna"
      },
      ...
    ]
    """
    @staticmethod
    def get(as_dict=False):
        args = parser.parse_args()
        result = formula_search(
            min_texts=args.get("n_texts_min"),
            max_texts=args.get("n_texts_max"),
            min_entries=args.get("n_entries_min"),
            max_entries=args.get("n_entries_max")
        )
        if as_dict:
            return result
        else:
            return jsonify(result)


class FormulaContexts(Resource):
    """
    Formula contexts API
    INPUT
    formula_id - unique formula (cluster) id
    OUTPUT
    [
      {
        "chapter_id": 6,
        "ngram_text": "ófeigur spurði ...",
        "paragraph_idx": 6,
        "sentence_idx": 1,
        "text_name": "Bandamanna saga - Konungsbók"
      },
      ...
    ]
    """
    @staticmethod
    def get(formula_id, as_dict=False):
        result = get_formula_contexts(formula_id)
        if as_dict:
            return result
        else:
            return jsonify(result)


if __name__ == '__main__':
    pass
