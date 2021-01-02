import flask
from discord_interactions import verify_key_decorator, InteractionType, InteractionResponseType
import requests
import json
import os

url = "https://discord.com/api/v8"

app = flask.Flask(__name__)
CLIENT_PUBLIC_KEY = ""
token = ""

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

@app.route("/api/slashcommands", methods=["POST"])
@verify_key_decorator(CLIENT_PUBLIC_KEY)
def test():
    if flask.request.json["type"] == InteractionType.APPLICATION_COMMAND:
        if flask.request.json["data"]["name"] == "test":
            return flask.jsonify({
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                "data": {
                    "content": "to jest komenda test"
                }
            })
        elif flask.request.json["data"]["name"] == "ping":
            return flask.jsonify({
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                "data": {
                    "content": "pong"
                }
            })
        elif flask.request.json["data"]["name"] == "avatar":
            if "options" in flask.request.json["data"]:
                id = flask.request.json["data"]["options"][0]["value"]
                avatar = requests.get(url + "/users/" + id, headers={"authorization": "Bot " + token}).json()["avatar"]
            else:
                id = flask.request.json["member"]["user"]["id"]
                avatar = flask.request.json["member"]["user"]["avatar"]
                
            avatar = "https://cdn.discordapp.com/avatars/" + id + "/" + avatar + ".png" + "?size=2048"
            return flask.jsonify({
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE,
                "data": {
                    "content": avatar
                }
            })

@app.route("/api/webhooks/topgg", methods=["POST"])
def topgg():
    if not flask.request.headers["authorization"] == "indextoslodkipedalek":
        return flask.jsonify({"success": False})

    user = flask.request.json["user"]
    user = discord.get_user(user)
        
    requests.post("https://discord.com/api/webhooks/794609230195720192/Rsw0hjp1BOUxpJnbSf7Lqx4JcggGBPLSrnReQ7bWr3K0LUtr42Tiqf1MWnYp8c90KUyF", json={
        "username": user["username"],
        "avatar_url": f"http://cdn.discordapp.com/avatars/{user['id']}/{user['avatar']}.png?size=2048",
        "content": f"Użytkownik {user['username']} zagłosował na bota!"
    })

    return flask.jsonify({"success": True})

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
