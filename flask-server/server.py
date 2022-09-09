from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:babyruby@localhost/baby-tracker'
db = SQLAlchemy(app)

class Event(db.Model):
    id 
# Members API Route
@app.route("/members")
def members():
    return {"members": ["Member1", "Member2", "Member3"]}

@app.route("/get_power", methods=['GET'])
def get_power():
    if request.method == 'GET':
        return Power().get_power()
    else:
        return jsonify("Method not allowed"), 405
    
    

if __name__ == "__main__":
    app.run(debug=True)