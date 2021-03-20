import flask
import os
from bs4 import BeautifulSoup
import random
import requests
import lxml
import cchardet

url = "https://discord.com/api/v8"
app = flask.Flask(__name__)
session = requests.Session()

@app.route("/", methods=["GET"])
def main():
    return flask.render_template("index.html")

@app.route("/discord", methods=["GET"])
def discord():
    return flask.redirect("https://discord.gg/kJuGceekR5")

@app.route("/invite", methods=["GET"])
def invite():
    return flask.redirect("https://discord.com/api/oauth2/authorize?client_id=705552952600952960&permissions=268561494&scope=bot")

@app.route("/sourcecode", methods=["GET"])
def sourcecode():
    return flask.redirect("https://github.com/CZUBIX/cenzura")

@app.route("/api/memes/jbzd", methods=["GET"])
def jzbdmemes():
    memes = []

    while not memes:
        memes_page = session.get(f"https://jbzd.com.pl/str/{random.randint(1, 235)}").content
        memes_soup = BeautifulSoup(memes_page, "lxml")

        memes = memes_soup.find_all("img", {"class":"article-image"})
        memes = [meme["src"] for meme in memes]

    return flask.jsonify(meme=random.choice(memes))

@app.route("/api/memes/kwejk", methods=["GET"])
def kwejkmemes():
    memes = []

    while not memes:
        memes_page = session.get(f"https://kwejk.pl/strona/{random.randint(4, 4000)}").content
        memes_soup = BeautifulSoup(memes_page, "lxml")

        memes = memes_soup.find_all("img", {"class":"full-image"})
        memes = [meme["src"] for meme in memes]

    return flask.jsonify(meme=random.choice(memes))

@app.route("/sitemap.xml")
def sitemap():
    return flask.send_from_directory("./", "sitemap.xml")

@app.route("/robots.txt")
def robots():
    return flask.send_from_directory("./", "robots.txt")

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == "static":
        filename = values.get("filename", None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values["q"] = int(os.stat(file_path).st_mtime)

    return flask.url_for(endpoint, **values)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2137)
