from flask import Flask, render_template, request
import requests
import os, sys
from logging.config import dictConfig
from flask.logging import default_handler


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': "%(message)s",
    }},
    'handlers': {'wsgi': {
        'class': 'logging.handlers.RotatingFileHandler',
        'filename': 'logs/applogs.log',
        'formatter': 'default',
        'backupCount': 3
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
app.logger.removeHandler(default_handler)


item_list = [
    ("Nike", 2000, "https://images.unsplash.com/photo-1542291026-7eec264c27ff?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MXx8c2hvZXxlbnwwfHwwfHw%3D&w=1000&q=80"),
    ("Adidas", 500, "https://media.istockphoto.com/photos/sport-shoes-on-isolated-white-background-picture-id956501428?k=20&m=956501428&s=612x612&w=0&h=UC4qdZa2iA0PJvv0RIBlJDyF80wxFyLPq4YWvZa30Sc="),
    ("Chuka", 1500, "https://media.istockphoto.com/photos/brown-leather-shoe-picture-id187310279?k=20&m=187310279&s=612x612&w=0&h=WDavpCxsLbj_PRpoY-3PsS2zvuP0Vk0Ci22sRLO9DzE="),
]
@app.get("/")
def index():

    items = [{"name":item[0], "price": int(item[1]), "image": item[2]} for item in item_list]
    return render_template("index.html", items=items)

@app.get("/logs")
def logs():
    return {"status": "OK"}

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    
@app.get('/break')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

if __name__ == "__main__":
    app.run(debug=os.environ.get("DEBUG") or True, host="0.0.0.0", port=5001)