from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    """Home endpoint that returns a greeting message"""
    return "Hello API"


@app.route('/add', methods=['GET'])
def add():
    """
    Add endpoint that takes two numbers from query parameters
    and returns their sum as JSON
    
    Query parameters:
    - a: first number
    - b: second number
    
    Example: /add?a=5&b=3
    Response: {"result": 8}
    """
    try:
        # Get query parameters
        a = request.args.get('a')
        b = request.args.get('b')
        
        # Validate that both parameters are provided
        if a is None or b is None:
            return jsonify({
                "error": "Missing parameters. Please provide both 'a' and 'b' query parameters."
            }), 400
        
        # Convert to float/int
        try:
            num_a = float(a)
            num_b = float(b)
        except ValueError:
            return jsonify({
                "error": "Invalid parameters. Both 'a' and 'b' must be numbers."
            }), 400
        
        # Calculate sum
        result = num_a + num_b
        
        # Return result as JSON
        return jsonify({
            "a": num_a,
            "b": num_b,
            "result": result
        })
    
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == '__main__':
    # Run on port 8000
    app.run(host='0.0.0.0', port=8000, debug=False)
