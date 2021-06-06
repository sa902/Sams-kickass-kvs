import os
import flask
import requests
from replit import db

app = flask.Flask(__name__)
sess = requests.Session()

@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "DELETE"]) #json
@app.route("/<path:path>", methods=["GET", "POST", "DELETE"]) # xml
def proxy(path):
  url = os.environ["REPLIT_DB_URL"]
  if flask.request.path != "/":
    url += flask.request.path

  req = requests.Request(flask.request.method, url, data=flask.request.form, params=flask.request.args).prepare()
  resp = sess.send(req)

  proxy_resp = flask.make_response(resp.text)
  proxy_resp.status_code = resp.status_code
  for k, v in resp.headers.items():
    proxy_resp.headers[k] = v

  return proxy_resp 
    

@app.route("/removeall")
def fullDelete():
	matches = db.prefix("")
	for i in matches:	
		print(i)
		del db[i]
	
	return "200"


@app.route("/countriesList")
def countriesList():
	value = db["COUNTRIES"]
	print(value)
	x = ["\""+i+"\"" for i in value]
	y = ( " [ " + ', '.join(x) + "]")
	return y

@app.route("/listall")
def listall():
	keys = db.keys()
	x = ["\""+i+"\"" for i in keys]
	y = ( " [ " + ', '.join(x) + "]")
	return y

@app.route("/webhook", methods=["GET", "POST", "DELETE"])
def webook():
	x = flask.request.args
	print(x['hub.challenge'])
	return x['hub.challenge']
 
# uncomment this to run:
app.run("0.0.0.0")



