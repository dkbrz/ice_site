# -*- coding: utf-8 -*-
"""
Search module:

1. API for search
2. Entry preprocessing for single-formula page
"""
from flask_restful import Resource, Api
from models import ClusterFilters as Cf, NgramEntries as Ne, TextContent as Tc

SENT_WINDOW = 3


def formula_search_to_dict(raw_result):
    """Dictionary form for API"""
    return [
        {
            "id": item.cluster_id,
            "text": item.text,
            "n_entries": item.n_entries,
            "n_texts": item.unique_text
        }
        for item in raw_result
    ]


def formula_search(min_texts, max_texts, min_entries, max_entries):
    """Filter search results"""

    result = Cf.query.filter(
        Cf.n_entries >= min_entries,
        Cf.n_entries <= max_entries,
        Cf.unique_text >= min_texts,
        Cf.unique_text <= max_texts
    ).group_by(
        Cf.short_ngram_id
    ).order_by(Cf.text).all()

    return formula_search_to_dict(result)


def render_formula_context(context, words):
    """Concat words from context and set span for formula itself"""
    result = []
    started, ended = False, False
    for word in words:
        is_formula = (
            word.sentence_unique == context.sentence_unique and
            context.start <= word.idx <= context.end
        )
        if is_formula and not started:
            result.append('<span class="f-page-formula">')
            started = True
        elif not is_formula and started and not ended:
            result.append('</span>')
            ended = True
        result.append(word.token.word_form)
    return " ".join(result)


def get_full_context(context):
    """Find extended context"""
    words = Tc.query.filter(
        Tc.text == context.text,
        Tc.sentence_unique >= (context.sentence_unique - SENT_WINDOW),
        Tc.sentence_unique <= (context.sentence_unique + SENT_WINDOW),
    ).all()
    return render_formula_context(context, words)


def get_formula_contexts(cluster_id):
    """Get formula contexts for formula page"""
    contexts = Ne.query.filter(
        Ne.cluster_id == cluster_id
    ).order_by(Ne.text, Ne.chapter, Ne.paragraph, Ne.sentence).all()
    return [
        {
            "text_name": c.text_obj.text_name,
            "chapter_id": c.chapter,
            "paragraph_idx": c.paragraph,
            "sentence_idx": c.sentence,
            "ngram_text": get_full_context(c)
        }
        for c in contexts
    ]


if __name__ == '__main__':
    pass
