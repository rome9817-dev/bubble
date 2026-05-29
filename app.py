from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Beer and Food Pairing Database
BEER_PAIRINGS = {
    "pizza": {
        "beers": ["IPA", "Pilsner", "Pale Ale"],
        "description": "Crisp and hoppy beers cut through the richness of cheese and sauce"
    },
    "burger": {
        "beers": ["Amber Ale", "Porter", "Brown Ale"],
        "description": "Robust beers complement the savory beef and toppings"
    },
    "fish": {
        "beers": ["Lager", "Wheat Beer", "Pilsner"],
        "description": "Light and refreshing beers enhance delicate fish flavors"
    },
    "steak": {
        "beers": ["Stout", "Porter", "Imperial Ale"],
        "description": "Full-bodied beers match the richness of red meat"
    },
    "chicken": {
        "beers": ["Blonde Ale", "Hefeweizen", "Saison"],
        "description": "Medium-bodied beers complement poultry without overpowering it"
    },
    "pasta": {
        "beers": ["Amber Ale", "IPA", "Pale Ale"],
        "description": "Balanced beers work well with tomato and cream-based sauces"
    },
    "salad": {
        "beers": ["Pilsner", "Wheat Beer", "Light Lager"],
        "description": "Light and crisp beers won't overwhelm fresh vegetables"
    },
    "asian": {
        "beers": ["Hefeweizen", "Pale Ale", "Lager"],
        "description": "Spicy Asian dishes pair well with aromatic and slightly sweet beers"
    },
    "mexican": {
        "beers": ["Pale Ale", "IPA", "Lager"],
        "description": "Hoppy or light beers complement spicy Mexican cuisine"
    },
    "barbecue": {
        "beers": ["Porter", "Brown Ale", "Amber Ale"],
        "description": "Smoky beers enhance the barbecue flavors"
    },
    "seafood": {
        "beers": ["Wheat Beer", "Pilsner", "Blonde Ale"],
        "description": "Light beers pair beautifully with fresh seafood"
    },
    "dessert": {
        "beers": ["Stout", "Porter", "Imperial IPA"],
        "description": "Rich beers with chocolate or caramel notes complement sweet treats"
    },
    "vegetarian": {
        "beers": ["IPA", "Pale Ale", "Saison"],
        "description": "Flavorful beers add depth to vegetable-based dishes"
    },
    "spicy": {
        "beers": ["Pale Ale", "Wheat Beer", "Light Lager"],
        "description": "Beers with residual sweetness cool down spicy heat"
    }
}

def get_beer_suggestion(food_item):
    """
    Get beer suggestions based on the food item
    """
    food_lower = food_item.lower().strip()
    
    # Direct match
    if food_lower in BEER_PAIRINGS:
        return BEER_PAIRINGS[food_lower]
    
    # Partial match
    for key, value in BEER_PAIRINGS.items():
        if key in food_lower or food_lower in key:
            return value
    
    # Default suggestion
    return {
        "beers": ["Pale Ale", "Lager", "Wheat Beer"],
        "description": "Try a versatile beer that works with most foods!"
    }

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/suggest-beer', methods=['POST'])
def suggest_beer():
    """API endpoint to get beer suggestions for a meal"""
    data = request.get_json()
    food_item = data.get('food', '')
    
    if not food_item:
        return jsonify({'error': 'Please provide a food item'}), 400
    
    suggestion = get_beer_suggestion(food_item)
    
    return jsonify({
        'food': food_item,
        'beers': suggestion['beers'],
        'description': suggestion['description']
    })

@app.route('/api/all-pairings', methods=['GET'])
def all_pairings():
    """API endpoint to get all available food and beer pairings"""
    return jsonify(BEER_PAIRINGS)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
