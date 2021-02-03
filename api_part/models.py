# -*- coding: utf-8 -*-
"""
DB Models:

Text
Token
TextContent - full corpus
ClusterFilters - search
NgramEntries - ngram entry coordinates
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()


class Text(db.Model):
    """
    Table with text names (names of sagas)
    """
    id = db.Column(db.Integer, primary_key=True)
    text_name = db.Column(db.Text)


class Token(db.Model):
    """
    Token
    word_form: form in text
    lemma: lemma
    """
    id = db.Column(db.Integer, primary_key=True)
    word_form = db.Column(db.Text)
    lemma = db.Column(db.Text)
    pos = db.Column(db.Text)


class TextContent(db.Model):
    """
    TextContent
    text: foreign key (Text)
    chapter: chapter index
    paragraph: index of paragraph in chapter
    sentence: index of sentence in paragraph
    sentence_unique: unique sentence ID (in all texts)

    token: token object (with lemma and word form)
    text_obj: text with id and name
    """
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Integer, ForeignKey("text.id"))
    chapter = db.Column(db.Integer)
    paragraph = db.Column(db.Integer)
    sentence = db.Column(db.Integer)
    sentence_unique = db.Column(db.Integer)
    idx = db.Column(db.Integer)
    token_id = db.Column(db.Integer, ForeignKey("token.id"))

    # relationships
    token = db.relationship("Token", uselist=False, primaryjoin="Token.id==TextContent.token_id")
    text_obj = db.relationship("Text", uselist=False, primaryjoin="Text.id==TextContent.text")


class ClusterFilters(db.Model):
    """
    ClusterFilters
    cluster_id: unique cluster identifier
    short_ngram_id: POS model
    cluster: cluster id within short_ngram group
    unique_text: number of texts where this cluster occurs
    n_entries: number of entries (in all texts)
    text: textual representation
    """
    id = db.Column(db.Integer, primary_key=True)
    cluster_id = db.Column(db.Integer)
    short_ngram_id = db.Column(db.Integer)
    cluster = db.Column(db.Integer)
    n_entries = db.Column(db.Integer)
    unique_text = db.Column(db.Integer)
    text = db.Column(db.Text)
    verb_text = db.Column(db.Text)


class NgramEntries(db.Model):
    """
    NgramEntries - coordinates of ngram entries

    start, end: word indices of the first and last words
    """
    id = db.Column(db.Integer, primary_key=True)
    short_ngram_id = db.Column(db.Integer)
    cluster_id = db.Column(db.Integer)
    text = db.Column(db.Integer, ForeignKey("text.id"))
    chapter = db.Column(db.Integer)
    paragraph = db.Column(db.Integer)
    sentence = db.Column(db.Integer)
    sentence_unique = db.Column(db.Integer)
    start = db.Column(db.Integer)
    end = db.Column(db.Integer)

    text_obj = db.relationship("Text", uselist=False, primaryjoin="Text.id==NgramEntries.text")
