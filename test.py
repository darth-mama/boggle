from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn('<p>High Score:', response.get_data(as_text=True))
            self.assertIn('Score:', response.get_data(as_text=True))
            self.assertIn('Seconds Left:', response.get_data(as_text=True))

    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["B", "A", "T", "C", "T"],
                                 ["B", "A", "T", "O", "T"],
                                 ["B", "A", "T", "N", "T"],
                                 ["B", "A", "T", "A", "T"],
                                 ["S", "A", "T", "C", "T"]]
        response = self.client.get('/check-word?word=can')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is in the dictionary"""

        self.client.get('/')
        response = self.client.get('/check-word?word=stoic')
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        """Test if word is on the board"""

        self.client.get('/')
        response = self.client.get(
            '/check-word?word=fsjdakfkldsfjdslkfjdlksf')
        self.assertEqual(response.json['result'], 'not-word')
