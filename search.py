# -*- coding: utf-8 -*-
"""
Search module:

1. API for search
2. Entry preprocessing for single-formula page
"""

from models import ClusterFilters as Cf, NgramEntries as Ne, TextContent as Tc

MIN, MAX = 0, 1000
SENT_WINDOW = 3


class Search:
    """Get information from DB"""

    def __init__(self):
        pass

    def formula_search(self, req):
        """Filter search results"""

        n_texts_min = req.values.get("n_texts_min", MIN)
        n_texts_max = req.values.get("n_texts_max", MAX)
        n_entries_min = req.values.get("n_entries_min", MIN)
        n_entries_max = req.values.get("n_entries_max", MAX)

        result = Cf.query.filter(
            Cf.n_entries >= n_entries_min,
            Cf.n_entries <= n_entries_max,
            Cf.unique_text >= n_texts_min,
            Cf.unique_text <= n_texts_max
        ).group_by(
            Cf.short_ngram_id
        ).order_by(Cf.text).all()

        return self.formula_search_to_dict(result)

    @staticmethod
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

    def get_formula_contexts(self, cluster_id):
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
                "ngram_text": self.get_full_context(c)
            }
            for c in contexts
        ]

    def get_full_context(self, context):
        """Find extended context"""
        words = Tc.query.filter(
            Tc.text == context.text,
            Tc.sentence_unique >= (context.sentence_unique - SENT_WINDOW),
            Tc.sentence_unique <= (context.sentence_unique + SENT_WINDOW),
        ).all()
        return self.render_formula_context(context, words)

    @staticmethod
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


if __name__ == '__main__':
    pass
