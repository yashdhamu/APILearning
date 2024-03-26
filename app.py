from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"Drink('{self.name}' - '{self.description}')"


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/drinks')
def get_drinks():
    drink = Drink.query.all()
    op = []
    for d in drink:
        op.append({'name': d.name, 'description': d.description})
    return {'drinks': op}

@app.route('/drinks/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    return jsonify({'name': drink.name, 'description': drink.description})


@app.route('/drinks', methods=['POST'])
def add_drink():
    drink = Drink(name=request.json['name'], description=request.json['description'])
    db.session.add(drink)
    db.session.commit()
    return {'id': drink.id}

@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drink(id):
    drink = Drink.query.get(id)
    if drink is None:
        return {'error': 'not found'}
    db.session.delete(drink)
    db.session.commit()
    return {'message': 'deleted'}

if __name__ == '__main__':
    app.run()
