from github_webhook import Webhook
from flask import Flask
import json
import requests

app = Flask(__name__)  # Standard Flask app
webhook = Webhook(app) # Defines '/postreceive' endpoint


@app.route("/")        # Standard Flask endpoint
def hello_world():
    return "Hello, World!"


@webhook.hook(event_type="pull_request")        # Defines a handler for the 'push' event
def on_push(data):
    #print(f"Got push with: {json.dumps(data, indent=2)}")
    action = data.get('action')
    print(f"action: {action}")
    pull_request = data.get('pull_request')
    if not action or not pull_request:
       return None
    merged = pull_request.get('merged')
    print(f"merged: {merged}")
    if not merged:
        return None
    files_url = pull_request.get("url") + "/files"
    print(f"files_url: {files_url}")
    print(json.dumps(do_github_api_call(files_url), indent=2))


def do_github_api_call(url):
    with open('./config.json') as fp:
        token = json.load(fp)["token"]
    headers = {f"Authorization": "token {token}"}
    return requests.get(url, headers=headers).json()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
