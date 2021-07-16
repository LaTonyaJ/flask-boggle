from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True


class TestFlask(TestCase):

    def test_homepage(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Seconds Left:', html)

    def test_valid_word(self):
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['board'] = [['D', 'O', 'G', 'G', 'G'],
                                    ['D', 'O', 'G', 'G', 'G'],
                                    ['D', 'O', 'G', 'G', 'G'],
                                    ['D', 'O', 'G', 'G', 'G'],
                                    ['D', 'O', 'G', 'G', 'G']]
            resp = client.get('/check-word?guess_input=dog')

            self.assertEqual(resp.json['Result'], 'ok')

    def test_invalid_word(self):
        with app.test_client() as client:
            client.get('/')
            resp = client.get('/check-word?guess_input=cat')

            self.assertEqual(resp.json['Result'], 'not-on-board')

    def test_invalid_word2(self):
        with app.test_client() as client:
            client.get('/')
            resp = client.get('/check-word?guess_input=yeaummno')

            self.assertEqual(resp.json['Result'], 'not-word')
