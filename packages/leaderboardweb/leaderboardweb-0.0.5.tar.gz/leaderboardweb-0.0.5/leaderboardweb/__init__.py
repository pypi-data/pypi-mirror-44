import flask

app = flask.Flask(__name__, static_url_path="")


@app.route("/")
def redirect_to_index():
    return flask.redirect(flask.url_for(redirect_to_index.__name__) + "index.html", code=301)
