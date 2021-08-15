import flask, os, io

app = flask.Flask(__name__)
images = {}

@app.route("/", methods=["GET"])
def main():
    return flask.render_template("index.html")

@app.route("/discord", methods=["GET"])
def discord():
    return flask.redirect("https://discord.gg/tDQURnVtGC", code=301)

@app.route("/invite", methods=["GET"])
def invite():
    return flask.redirect("https://discord.com/api/oauth2/authorize?client_id=705552952600952960&permissions=268561494&scope=bot", code=301)

@app.route("/sourcecode", methods=["GET"])
def sourcecode():
    return flask.redirect("https://github.com/CZUBIX/cenzura", code=301)

@app.route("/ktg", methods=["POST"])
def ktg_post():
    images[str(len(images) + 1)] = flask.request.files["file"].read()
    return flask.jsonify(code=len(images)), 201

@app.route("/ktg/<code>", methods=["GET"])
def ktg_get(code):
    return flask.send_file(io.BytesIO(images[code]), mimetype="image/jpeg", as_attachment=True, attachment_filename=f"{code}.jpg")

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
