from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

pokedex = [{
    'number': '14',
    'name': 'Kakuna',
    'type': ['bug', 'poison'],
    'weaknesses': ['fire', 'flying', 'psychic', 'rock'],
}, {
    'number': '16',
    'name': 'Pidgey',
    'type': ['normal', 'flying'],
    'weaknesses': ['electric', 'ice', 'rock'],
}, {
    'number': '43',
    'name': 'Dugtrio',
    'type': ['ground'],
    'weaknesses': ['grass', 'ice', 'water'],
}]


def list_of_strings(value):
    all_str = isinstance(value, list) and all([isinstance(a, str) for a in value])
    if not all_str:
        raise ValueError("List or strings required")
    return value


def get_pokemon_args():
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True, type=str, location='json')
    parser.add_argument('number', required=True, type=int, location='json')
    parser.add_argument('type', required=True, type=list_of_strings, location='json')
    parser.add_argument('weaknesses', required=True, type=list_of_strings, location='json')
    return parser.parse_args(strict=True)


class Pokemon(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('number', required=False, type=str, location='args')
        args = parser.parse_args(strict=True)
        number = args.get('number')
        # could have?... if number:
        if number is not None:
            if number in [a['number'] for a in pokedex]:
                return [a for a in pokedex if a['number'] == number][0]
            else:
                return {}
        return pokedex

    def post(self):
        args = get_pokemon_args()

        new_pokemon = {
            'name': args['name'],
            'number': args['number'],
            'type': args['type'],
            'weaknesses': args['weaknesses']
        }

        new_number = new_pokemon['number']
        all_numbers = [a['number'] for a in pokedex]
        if new_number in all_numbers:
            return {}
        pokedex.append(new_pokemon)
        return pokedex[-1]

    def put(self):
        args = get_pokemon_args()

        new_pokemon = {
            'name': args['name'],
            'number': args['number'],
            'type': args['type'],
            'weaknesses': args['weaknesses']
        }

        new_number = new_pokemon['number']
        all_numbers = [a['number'] for a in pokedex]
        if new_number not in all_numbers:
            return {}
        index = all_numbers.index(new_number)
        pokedex[index] = new_pokemon
        
        return pokedex[index]


api.add_resource(Pokemon, '/api/v1/pokemon')

if __name__ == '__main__':
    app.run(port=8000, debug=True)
