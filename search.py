# from models import A


class Search:

    def __init__(self):
        pass

    def formula_search(self, request):
        result = []
        return self.formula_to_dict(result)

    @staticmethod
    def formula_to_dict(raw_result):
        result = []
        for item in raw_result:
            result.append({
                "verb": None,
                "clusters": [
                    {
                        "mask": None,
                        "cluster": None,
                        "id": None
                    }
                    for i in []
                ]
            })
        return result

    def formula_contexts(self, formula_id):
        contexts = []
        result = []
        for context in contexts:
            contexts.append({
                "text_id": None,
                "chapter_id": None,
                "paragraph_idx": None,
                "sentence_idx": None,
                "text": self.render_text(context.words)
            })
        return result

    @staticmethod
    def render_text(words):
        result = []
        started, ended = False, False
        for word in words:
            if word.is_formula and not started:
                result += '<span class="f-page-formula"'
                started = True
            elif not word.is_formula and not ended:
                result += '</span>'
            result.append(word.wordform)
        return " ".join(result)
