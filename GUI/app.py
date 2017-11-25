import os
from flask import Flask, render_template, json, url_for, jsonify
app = Flask(__name__)
f_json = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'config.json'))


@app.route('/')
# @app.route('/<name>')
def hello(name=None):
	data = json.load(open(f_json))
	return render_template('index.html', name=name,data=data)
@app.route('/loop')
def loop():
	data = json.load(open(f_json))
	# data = jsonify(f_json)
	return render_template('loop.html', data=data)
	# return jsonify(data)

@app.route('/json')
def a_json():
	return render_template('json.html')

@app.route('/api/json')
def l_json():
	data = json.load(open(f_json))
	return jsonify(data)

@app.errorhandler(404)
def page_not_found(e):
    return "SORRY 404", 404
    # return render_template('404.html'), 404

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)

