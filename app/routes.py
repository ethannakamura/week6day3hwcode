from app import app
from flask import render_template
from flask_login import login_required

@app.route('/')
def home():
    import requests as r
    data = r.get('https://pokeapi.co/api/v2/pokedex/hoenn')
    if data.status_code == 200:
        data = data.json()
        context={
            'name': data['name'].title(),
            'poke': data['pokemon_entries']
        }
    return render_template('index.html', **context)

@app.route('/about')
@login_required
def about():
    context = {
        'teacher': 'Sam',
        'students': ['Zaki', 'Vanessa', 'Paul', 'Shaharima', 'Mohammed', 'Ezekiel', 'Adrian', 'Ethan']
    }
    return render_template('about.html', classname='Foxes78', **context)