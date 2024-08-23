from flask import request, Flask
import json

app = Flask(__name__)

@app.route('/submit', methods = ['POST'])
def submit():
    print(f"data: {request.values}")
    decoded = request.get_json()

    return f"data:{request.values['data']}"


