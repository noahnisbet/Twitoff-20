"""Example of a one file Flask application that uses and API and Database"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(app)


@app.route('/')  # Root endpoint
def root():
    astro_data = Astros.query.all()[0]
    return "There are {} astros in space".format(astro_data.num_astros)


@app.route('/refresh')  # refresh endpoint
def refresh():
    DB.drop_all()
    DB.create_all()
    request = requests.get("http://api.open-notify.org/astros.json")
    astro_data = request.json()
    num_astros = astro_data['number']
    # Save to SQL DB
    record = Astros(num_astros=num_astros)
    DB.session.add(record)
    DB.session.commit()
    return "Database has been updated!"


# Database table "Astros"
class Astros(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    num_astros = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return "# of astros: {}".format(self.num_astros)
