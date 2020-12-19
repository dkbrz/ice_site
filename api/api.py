# -*- coding: utf-8 -*-
"""
Search module:

1. API for search
2. Entry preprocessing for single-formula page
"""
from flask import jsonify
from flask_restful import Resource, reqparse
from api.search import formula_search, get_formula_contexts

MIN, MAX = 0, 1000

parser = reqparse.RequestParser()
parser.add_argument('n_texts_min', type=int)
parser.add_argument('n_texts_max', type=int)
parser.add_argument('n_entries_min', type=int)
parser.add_argument('n_entries_max', type=int)


class FormulaSearch(Resource):

    def get(self):
        args = parser.parse_args()
        return formula_search(
                min_texts=args.get("n_texts_min", MIN),
                max_texts=args.get("n_texts_max", MAX),
                min_entries=args.get("n_entries_min", MIN),
                max_entries=args.get("n_entries_max", MAX)
            )


class FormulaContexts(Resource):

    def get(self, formula_id):
        return get_formula_contexts(formula_id)


if __name__ == '__main__':
    pass
