import flask
import json
import os

url = "https://discord.com/api/v8"

app = flask.Flask(__name__)

@app.route("/", methods=["GET"])
def main():
    return flask.render_template("index.html")

@app.route("/docs", methods=["GET"])
def docs():
    with open("/cenzurabeta/commands.json", "r") as f:
        commands = json.load(f)

    blacklist = ["help", "dev"]

    categories = {}
    for command in commands:
        commands[command]["name"] = command
        if not commands[command]["category"] in categories:
            categories[commands[command]["category"]] = []

    for command in commands:
        categories[commands[command]["category"]].append(commands[command])

    for category in blacklist:
        del categories[category]

    return flask.render_template("docs.html", categories=categories)

@app.route("/sitemap.xml")
def sitemap():
    return flask.send_from_directory("./", "sitemap.xml")

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == "static":
        filename = values.get("filename", None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values["q"] = int(os.stat(file_path).st_mtime)

    return flask.url_for(endpoint, **values)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2137)