from flask import Flask, request, abort, redirect, jsonify
import re
import jwt
import datetime
app = Flask(__name__)

JWT_TOKEN_SECRET = "Some_very_good_password_secret_like_thing_or_so"
urls = {'0':'https://www.google.com'}

shared = {'counter': 0}

regex = re.compile(
        r'^http(s)?://[a-zA-Z0-9\-]+\.[a-zA-Z0-9\-\.]{2,}'
        ) 

def request_is_authenticated(request):
    data = {}
    try:
        token = request.headers.get("x-access-token")
        data = jwt.decode(token, JWT_TOKEN_SECRET, algorithms=['HS256'])
    except:
        return False
    return "username" in data    


@app.route("/<id>",methods=['GET','PUT','DELETE'])
def route_id(id):
    if id not in urls:
        abort(404)
    if request.method == "GET":
        return redirect (urls[id], code=301)
    
    if not request_is_authenticated(request):
        return "forbidden", 403
    if request.method == "PUT":
        if "url" not in request.form:
            abort(400)
        if not re.match(regex, request.form['url']): # check if input is URL
            abort(400)
        urls[id] = request.form['url']
        return ""
    if request.method == "DELETE":
        del urls[id]
        return "", 204

@app.route("/",methods=['GET','POST','DELETE'])
def route_url():
    if request.method == "GET":
        return jsonify(list(urls.keys()))
    
    if not request_is_authenticated(request):
        return "forbidden", 403

    if request.method == "POST":
        if "url" not in request.form:
            abort(400)
        if not re.match(regex, request.form['url']): # check if input is URL
            abort(400)
        id = None
        for key in urls:
            if urls[key] == request.form['url']:
                id = key
                break
        if id is None:
            id = shared['counter']
            shared['counter'] +=1
            urls[str(id)]=request.form['url']
        return str(id), 201

    if request.method == "DELETE":
        urls.clear()
        return '', 204    

app.run(host='0.0.0.0', port='80')