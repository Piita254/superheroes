from flask import Flask,jsonify,request,make_response
from flask_migrate import Migrate

from models import db, SuperHero, Power, Hero

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Initialize the database with the app
db.init_app(app)

migrate = Migrate(app, db)
@app.route('/')
def home():
    return '<h1> This is my home page </h1>'
# GET /heroes - List all heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict(only=('id', 'name', 'super_name')) for hero in heroes])

# GET /heroes/:id - Get hero by ID
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if hero:
        return jsonify({
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name,
            "hero_powers": [
                {
                    "hero_id": superhero.hero_id,
                    "id": superhero.id,
                    "power_id": superhero.power_id,
                    "strength": superhero.strength,
                    "power": superhero.power.to_dict(only=('id', 'name', 'description'))
                } for superhero in hero.superheroes
            ]
        })
    return jsonify({"error": "Hero not found"}), 404

# GET /powers - List all powers

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()  

    powers_list = []
    
    for power in powers:
        power_dict = {
            "description": power.description,
            "id": power.id,
            "name": power.name
        }
        powers_list.append(power_dict)

    return (powers_list), 200

# GET /powers/:id - Get power by ID
@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get(id)

    if power is None:
        return make_response({"error": "Power not found"}, 404)

    power_dict = {
        "id": power.id,
        "name": power.name,
        "description": power.description
    }

    return (power_dict), 200
# PATCH /powers/:id - Update power description
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power:
        data = request.get_json()
        if 'description' in data and data['description']:
            power.description = data['description']
            db.session.commit()
            return jsonify(power.to_dict(only=('id', 'name', 'description')))
        return jsonify({"errors": ["validation errors"]}), 400
    return jsonify({"error": "Power not found"}), 404

# POST /hero_powers - Create a new HeroPower
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')
    strength = data.get('strength')

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if hero and power and strength:
        new_hero_power = SuperHero(strength=strength, hero_id=hero_id, power_id=power_id)
        db.session.add(new_hero_power)
        db.session.commit()
        return jsonify({
            "id": new_hero_power.id,
            "hero_id": new_hero_power.hero_id,
            "power_id": new_hero_power.power_id,
            "strength": new_hero_power.strength,
            "hero": hero.to_dict(only=('id', 'name', 'super_name')),
            "power": power.to_dict(only=('id', 'name', 'description'))
        }), 201
    return jsonify({"errors": ["validation errors"]}), 400

if __name__ == '__main__':
    app.run(debug=True)

