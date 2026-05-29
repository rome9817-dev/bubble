# 🍺 Beer & Food Pairing Web App

A web application that suggests the perfect beer pairings for your meals.

## Features

✅ Search for beer suggestions based on food items  
✅ Browse all available food and beer pairings  
✅ Beautiful, responsive UI  
✅ RESTful API backend  

## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

The app will start on `http://localhost:5000`

### 3. Open in Browser

Navigate to `http://localhost:5000` in your web browser.

## Usage

1. **Type a food item** (e.g., pizza, steak, fish, Asian food)
2. **Click "Find Beer"** or press Enter
3. Get instant beer pairing suggestions with descriptions
4. **Browse All Pairings** to see all available combinations

## Available Food Pairings

- Pizza
- Burger
- Fish
- Steak
- Chicken
- Pasta
- Salad
- Asian
- Mexican
- Barbecue
- Seafood
- Dessert
- Vegetarian
- Spicy dishes

## API Endpoints

### Get Beer Suggestion
```
POST /api/suggest-beer
Content-Type: application/json

{
  "food": "pizza"
}
```

Response:
```json
{
  "food": "pizza",
  "beers": ["IPA", "Pilsner", "Pale Ale"],
  "description": "Crisp and hoppy beers cut through the richness of cheese and sauce"
}
```

### Get All Pairings
```
GET /api/all-pairings
```

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Server**: Flask development server

## Project Structure

```
bubble/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── templates/
    └── index.html        # Frontend UI
```

## Tips for Enhancement

- Add more food and beer pairing data
- Implement a database (SQLite, PostgreSQL) to store pairings
- Add user ratings and reviews for pairings
- Integrate real beer databases (e.g., BreweryDB API)
- Add user authentication for saving favorite pairings
- Deploy to a cloud platform (Heroku, AWS, etc.) 
