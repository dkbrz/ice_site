import unittest
from api_part.app import app, db
from api_part.models import ClusterFilters


class TestCase(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ice_site_test.db'

        self.app = app.test_client()

        db.create_all()

        formula1 = ClusterFilters(
            id=1, cluster_id=1, short_ngram_id=1, cluster=1, n_entries=5,
            unique_text=1, text="test text", verb_text="test"
        )
        db.session.add(formula1)
        formula2 = ClusterFilters(
            id=2, cluster_id=2, short_ngram_id=2, cluster=1, n_entries=1,
            unique_text=2, text="test text 2", verb_text="test"
        )
        db.session.add(formula2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_ngrams(self):
        response = self.app.get('/api_part/formula_search')
        predicted = [
            {"id": 1, "n_entries": 5, "n_texts": 1, "text": "test text", "verb_text": "test"},
            {"id": 2, "n_entries": 1, "n_texts": 2, "text": "test text 2", "verb_text": "test"},
        ]

        self.assertEqual(200, response.status_code)
        self.assertEqual(predicted, response.json)

    def test_filtered_ngrams(self):

        response = self.app.get('/api_part/formula_search', data={"n_texts_min": 2, "n_entries_min": 5})

        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.json)

    def test_formula_contexts_empty(self):

        response = self.app.get('/api_part/contexts/0')

        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.json)

    def test_404(self):

        response = self.app.get('/api_part')

        self.assertEqual(404, response.status_code)


if __name__ == '__main__':
    unittest.main()
