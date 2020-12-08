from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, PrimaryKeyConstraint

db = SQLAlchemy()


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word_form = db.Column(db.Text)
    lemma = db.Column(db.Text)


class TextContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Integer)
    chapter = db.Column(db.Integer)
    paragraph = db.Column(db.Integer)
    sentence = db.Column(db.Integer)
    sentence_unique = db.Column(db.Integer)
    idx = db.Column(db.Integer)
    token_id = db.Column(db.Integer, ForeignKey("token.id"))

    # relationships
    token = db.relationship("Token", uselist=False, primaryjoin="Token.id==TextContent.token_id")


class ClusterFilters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cluster_id = db.Column(db.Integer)
    short_ngram_id = db.Column(db.Integer)
    cluster = db.Column(db.Integer)
    n_entries = db.Column(db.Integer)
    unique_text = db.Column(db.Integer)
    text = db.Column(db.Text)


class NgramEntries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_ngram_id = db.Column(db.Integer)
    cluster_id = db.Column(db.Integer)
    sentence_unique = db.Column(db.Integer)
    start = db.Column(db.Integer)
    end = db.Column(db.Integer)

