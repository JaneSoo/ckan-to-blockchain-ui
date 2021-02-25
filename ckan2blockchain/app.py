from flask import Flask, render_template, jsonify, make_response, request
import hashlib, json, time, sys, urllib.request, urllib.parse
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-packages', methods=["POST"])
def get_packages():
    url = request.get_json()['url']
    res = urllib.request.urlopen(url).read()
    res_json = json.loads(res.decode())
    res = make_response(jsonify({"package_lists": res_json['result']}), 200)
    return res

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)