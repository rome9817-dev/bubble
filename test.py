import unittest
import json
from app import app, get_beer_suggestion, BEER_PAIRINGS


class BeerPairingTestCase(unittest.TestCase):
    """Test cases for the Beer Pairing Web App"""

    def setUp(self):
        """Set up test client before each test"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_app_exists(self):
        """Test that the app exists"""
        self.assertIsNotNone(self.app)

    def test_index_page_loads(self):
        """Test that the index page loads successfully"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Beer Pairing', response.data)

    def test_get_beer_suggestion_direct_match(self):
        """Test getting beer suggestion for a direct food match"""
        suggestion = get_beer_suggestion('pizza')
        self.assertIn('beers', suggestion)
        self.assertIn('description', suggestion)
        self.assertEqual(len(suggestion['beers']), 3)
        self.assertIn('IPA', suggestion['beers'])

    def test_get_beer_suggestion_partial_match(self):
        """Test getting beer suggestion for partial food match"""
        suggestion = get_beer_suggestion('asian')
        self.assertIn('beers', suggestion)
        self.assertIsNotNone(suggestion['description'])

    def test_get_beer_suggestion_case_insensitive(self):
        """Test that food matching is case insensitive"""
        suggestion_lower = get_beer_suggestion('pizza')
        suggestion_upper = get_beer_suggestion('PIZZA')
        self.assertEqual(suggestion_lower['beers'], suggestion_upper['beers'])

    def test_get_beer_suggestion_with_spaces(self):
        """Test that extra spaces are handled correctly"""
        suggestion = get_beer_suggestion('  pizza  ')
        self.assertIn('beers', suggestion)
        self.assertIn('IPA', suggestion['beers'])

    def test_get_beer_suggestion_unknown_food(self):
        """Test getting beer suggestion for unknown food item"""
        suggestion = get_beer_suggestion('unknown_food_xyz')
        self.assertIn('beers', suggestion)
        # Should return default suggestion
        self.assertEqual(len(suggestion['beers']), 3)

    def test_api_suggest_beer_post_success(self):
        """Test POST endpoint for beer suggestions"""
        response = self.client.post('/api/suggest-beer',
                                    data=json.dumps({'food': 'steak'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['food'], 'steak')
        self.assertIn('beers', data)
        self.assertIn('description', data)

    def test_api_suggest_beer_missing_food(self):
        """Test POST endpoint without food parameter"""
        response = self.client.post('/api/suggest-beer',
                                    data=json.dumps({}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_api_suggest_beer_empty_food(self):
        """Test POST endpoint with empty food string"""
        response = self.client.post('/api/suggest-beer',
                                    data=json.dumps({'food': ''}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_api_all_pairings_get(self):
        """Test GET endpoint for all pairings"""
        response = self.client.get('/api/all-pairings')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        # Check that data contains expected keys
        self.assertIn('pizza', data)
        self.assertIn('steak', data)
        self.assertIn('fish', data)

    def test_all_pairings_structure(self):
        """Test the structure of all pairings data"""
        for food, pairing in BEER_PAIRINGS.items():
            self.assertIn('beers', pairing)
            self.assertIn('description', pairing)
            self.assertIsInstance(pairing['beers'], list)
            self.assertGreater(len(pairing['beers']), 0)
            self.assertIsInstance(pairing['description'], str)

    def test_beer_suggestions_contain_valid_types(self):
        """Test that all beer suggestions contain valid beer types"""
        valid_beer_types = ['IPA', 'Pilsner', 'Lager', 'Stout', 'Porter', 
                           'Pale Ale', 'Amber Ale', 'Brown Ale', 'Blonde Ale',
                           'Wheat Beer', 'Hefeweizen', 'Saison', 'Imperial Ale',
                           'Imperial IPA', 'Light Lager']
        
        for food, pairing in BEER_PAIRINGS.items():
            for beer in pairing['beers']:
                self.assertIn(beer, valid_beer_types,
                            f"Unknown beer type '{beer}' for food '{food}'")

    def test_pizza_suggestions(self):
        """Test specific pizza pairing"""
        suggestion = get_beer_suggestion('pizza')
        self.assertEqual(suggestion['beers'], ['IPA', 'Pilsner', 'Pale Ale'])
        self.assertIn('cheese', suggestion['description'].lower())

    def test_steak_suggestions(self):
        """Test specific steak pairing"""
        suggestion = get_beer_suggestion('steak')
        self.assertEqual(suggestion['beers'], ['Stout', 'Porter', 'Imperial Ale'])
        self.assertIn('red meat', suggestion['description'].lower())

    def test_fish_suggestions(self):
        """Test specific fish pairing"""
        suggestion = get_beer_suggestion('fish')
        self.assertIn('Lager', suggestion['beers'])
        self.assertIn('light', suggestion['description'].lower())

    def test_burger_suggestions(self):
        """Test specific burger pairing"""
        suggestion = get_beer_suggestion('burger')
        self.assertIn('Amber Ale', suggestion['beers'])

    def test_api_response_json_format(self):
        """Test that API responses are proper JSON"""
        response = self.client.post('/api/suggest-beer',
                                    data=json.dumps({'food': 'pizza'}),
                                    content_type='application/json')
        data = json.loads(response.data)
        # Verify structure
        self.assertIn('food', data)
        self.assertIn('beers', data)
        self.assertIn('description', data)

    def test_multiple_food_queries(self):
        """Test multiple food queries to ensure consistency"""
        foods = ['pizza', 'steak', 'fish', 'chicken', 'asian']
        for food in foods:
            response = self.client.post('/api/suggest-beer',
                                        data=json.dumps({'food': food}),
                                        content_type='application/json')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIsNotNone(data['beers'])
            self.assertGreater(len(data['beers']), 0)

    def test_special_characters_in_food(self):
        """Test handling of special characters"""
        response = self.client.post('/api/suggest-beer',
                                    data=json.dumps({'food': 'pizza & pasta'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('beers', data)


class BeerDatabaseTestCase(unittest.TestCase):
    """Test cases for the beer pairing database"""

    def test_pizza_in_database(self):
        """Test that pizza is in the database"""
        self.assertIn('pizza', BEER_PAIRINGS)

    def test_all_foods_have_descriptions(self):
        """Test that all foods have descriptions"""
        for food, details in BEER_PAIRINGS.items():
            self.assertTrue(len(details['description']) > 0,
                          f"No description for {food}")

    def test_all_foods_have_beers(self):
        """Test that all foods have beer recommendations"""
        for food, details in BEER_PAIRINGS.items():
            self.assertGreater(len(details['beers']), 0,
                             f"No beers recommended for {food}")

    def test_database_has_minimum_foods(self):
        """Test that database has at least 10 food options"""
        self.assertGreater(len(BEER_PAIRINGS), 10)


class ContentSecurityTestCase(unittest.TestCase):
    """Test cases for content security"""

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_html_injection_prevention(self):
        """Test that HTML injection is handled safely"""
        response = self.client.post('/api/suggest-beer',
                                    data=json.dumps({'food': '<script>alert("xss")</script>'}),
                                    content_type='application/json')
        # Should still return 200 and handle gracefully
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsNotNone(data)


if __name__ == '__main__':
    unittest.main()
