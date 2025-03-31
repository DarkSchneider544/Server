from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Enhanced HTML template for the home page with embedded CSS styling
home_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Interactive Calculator Service</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to right, #83a4d4, #b6fbff);
            margin: 0;
            padding: 0;
            color: #333;
        }
        .container {
            width: 90%;
            max-width: 500px;
            margin: 50px auto;
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            padding: 20px;
        }
        h1 {
            text-align: center;
            color: #4a90e2;
        }
        form {
            display: flex;
            flex-direction: column;
        }
        label {
            margin-top: 10px;
            font-weight: bold;
        }
        input[type="text"] {
            padding: 8px;
            margin-top: 5px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button {
            margin-top: 20px;
            padding: 10px;
            background-color: #4a90e2;
            color: #fff;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover {
            background-color: #357ab7;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            font-size: 0.9em;
            color: #777;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Interactive Calculator</h1>
        <p>Please enter two numbers and an operator to perform a calculation.</p>
        <form action="/compute" method="post">
            <label for="number1">Number 1:</label>
            <input type="text" id="number1" name="number1" required>
            
            <label for="operator">Operator (+, -, *, /):</label>
            <input type="text" id="operator" name="operator" required>
            
            <label for="number2">Number 2:</label>
            <input type="text" id="number2" name="number2" required>
            
            <button type="submit">Compute</button>
        </form>
        <div class="footer">
            &copy; 2025 Interactive Calculator Service
        </div>
    </div>
</body>
</html>
"""

# Enhanced HTML template for displaying the result with CSS styling
result_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Calculation Result</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to right, #b6fbff, #83a4d4);
            margin: 0;
            padding: 0;
            color: #333;
        }
        .container {
            width: 90%;
            max-width: 500px;
            margin: 50px auto;
            background: #fff;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            padding: 20px;
            text-align: center;
        }
        h1 {
            color: #4a90e2;
        }
        p {
            font-size: 1.2em;
        }
        a {
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            background-color: #4a90e2;
            color: #fff;
            text-decoration: none;
            border-radius: 4px;
        }
        a:hover {
            background-color: #357ab7;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            font-size: 0.9em;
            color: #777;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Calculation Result</h1>
        <p>{{ number1 }} {{ operator }} {{ number2 }} = <strong>{{ result }}</strong></p>
        <a href="/">Perform Another Calculation</a>
        <div class="footer">
            &copy; 2025 Interactive Calculator Service
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(home_page)

@app.route('/compute', methods=['POST'])
def compute():
    try:
        number1 = float(request.form.get('number1'))
        number2 = float(request.form.get('number2'))
        operator = request.form.get('operator').strip()
    except (ValueError, TypeError):
        return "Invalid input. Please ensure numbers are valid.", 400

    if operator == '+':
        result = number1 + number2
    elif operator == '-':
        result = number1 - number2
    elif operator == '*':
        result = number1 * number2
    elif operator == '/':
        if number2 == 0:
            return "Error: Division by zero.", 400
        result = number1 / number2
    else:
        return "Invalid operator. Please use one of: +, -, *, /", 400

    return render_template_string(result_page, number1=number1, number2=number2, operator=operator, result=result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
