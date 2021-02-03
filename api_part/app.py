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
from flask import Flask
from flask_restful import Api
from api_part.models import db
from api_part.api import FormulaSearch, FormulaContexts


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ice_site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db.app = app
db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(FormulaSearch, '/api_part/formula_search')
api.add_resource(FormulaContexts, '/api_part/contexts/<formula_id>')


if __name__ == '__main__':
    app.run(debug=True, port=5010)