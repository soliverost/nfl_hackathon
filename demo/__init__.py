import pkg_resources

from os import environ, path
from flask import Flask, render_template, send_from_directory

import pandas

from buildui import make_ui

here = path.abspath(path.dirname(__file__))

app = Flask(__name__)

datafiles = {
    "locations": here+"/../data/all_game_positions.csv",
    "players": here+"/../data/all_players.csv",
    "scores": here+'/../data/fatigue_scores.csv',
    "distance": here+"/../data/distance_metrics.csv"
}

ui = make_ui(datafiles)
ui.render_layout(app, "./assets/scripts/app2.js")

TITLE = "NFL Hackathon"

scripts = [
    # "./bower_components/jquery/dist/jquery.min.js",
    "./plotly.js"
]

css = [
    "./bower_components/bootstrap/dist/css/bootstrap.min.css",
    "./css/main.css"
]

@app.route('/', methods=["GET"])
def index():
    _scripts = ["./js/bundle.js"]
    return render_template('index.html',
        page_scripts=_scripts,
        base_scripts=scripts,
        css=css,
        title=TITLE)

if __name__ == "__main__":
    app.run(debug=True)
