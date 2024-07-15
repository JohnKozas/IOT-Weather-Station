from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@192.168.1.6:5432/postgres'

db = SQLAlchemy(app)

class weatherproject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Integer, nullable=False)
    humidity = db.Column(db.Integer, nullable=False)
    pressure = db.Column(db.Integer, nullable=False)
    light = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    WeatherProject = weatherproject.query.get(1)
    return render_template('index.html', WeatherProject=WeatherProject)

@app.route('/projects/')
def projects():
    return '<p>WeatherProject.temperature<p>'

@app.route('/about')
def about():
    return 'The about page'


if __name__ == '__main__':
    app.run(debug=True)
