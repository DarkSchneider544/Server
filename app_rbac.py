from flask import Flask, request, jsonify, render_template_string, abort
from functools import wraps

app = Flask(__name__)

# Simulated user database keyed by access token
# In a real scenario, this info would be retrieved from an identity provider.
USERS = {
    "token-user": {"username": "personA", "roles": ["user"]},
    "token-admin": {"username": "tirth", "roles": ["admin"]},
    "token-both": {"username": "personB", "roles": ["user", "admin"]},
}

# RBAC decorator that checks if the user's roles include at least one of the allowed roles.
def require_role(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Expect an Authorization header in the form: "Bearer <token>"
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                abort(401, description="Missing or invalid Authorization header")
            token = auth_header.split(" ")[1]
            user = USERS.get(token)
            if not user:
                abort(401, description="Invalid access token")
            # Check if the user has at least one allowed role
            if not any(role in user["roles"] for role in allowed_roles):
                abort(403, description="Insufficient permissions")
            # Optionally, attach the user info to the request context
            request.user = user
            return f(*args, **kwargs)
        return wrapper
    return decorator

# Enhanced HTML templates for home and result pages remain unchanged.
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

# Protect /compute with RBAC: only users with the "user" role can perform calculations.
@app.route('/compute', methods=['POST'])
@require_role("user")
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

#curl -X POST http://127.0.0.1:5000/compute \
 #    -H "Authorization: Bearer token-user" \
#     -d "number1=10&operator=+&number2=5"
