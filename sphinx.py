#!flask/bin/python

from flask import Flask, request, abort, make_response
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
from os import listdir, path, remove
from importlib import import_module
import uuid
import atexit

def load_riddles():
    riddles = {}
    riddle_files = map((lambda r: path.splitext(r)[0]), listdir('riddles'))
    for riddle in riddle_files:
        if not riddle == '__init__':
            riddles[riddle] = import_module('riddles.%s' % riddle)
    return riddles

def import_code(name,code):
    import sys,imp

    module = imp.new_module(name)

    exec code in module.__dict__

    return module

def api():
    app = Flask(__name__)

    riddles = load_riddles()
    questions = {}

    @app.route('/', methods=['GET'])
    def index():
        with open('README.md', 'r') as readme:
            return make_response(readme.read(), 200)

    @app.route('/riddles', methods=['GET'])
    def list_riddles():
        return make_response(str(riddles.keys()), 200)

    @app.route('/<riddle>/description', methods=['GET'])
    def description(riddle):
        if riddle in riddles:
            return make_response(riddles[riddle].description(), 200)
        else:
            return abort(404)

    @app.route('/<riddle>/question', methods=['GET'])
    def question(riddle):
        if riddle in riddles:
            question_id = uuid.uuid1().hex
            (question, answer) = riddles[riddle].question()
            questions[question_id] = answer

            response = make_response(question, 200)
            response.headers.extend({'X-Question-Id': question_id})
            return response
        else:
            return abort(404)

    @app.route('/<riddle>/answer', methods=['POST'])
    def answer(riddle):
        if not request.json or not 'answer' in request.json or not 'X-Question-Id' in request.headers:
            return abort(400)
        if riddle in riddles and request.headers['X-Question-Id'] in questions:
            answer = request.json['answer']
            question_id = request.headers['X-Question-Id']
            if answer == questions.pop(question_id):
                return make_response('Correct!', 200)
            else:
                return make_response('Incorrect', 200)
        else:
            return abort(404)

    @app.route('/<riddle>/upload', methods=['POST'])
    def upload(riddle):
        if not request.data:
            return abort(400)
        if not riddle in riddles:
            module = import_code(riddle, request.data)
            riddles[riddle] = module
            return make_response(str(riddles.keys()), 200)
        else:
            return abort(400)

    return app

def remove_pyc():
    files = listdir('riddles')

    for item in files:
        if item.endswith(".pyc"):
            remove(path.join('riddles', item))

if __name__ == '__main__':
    atexit.register(remove_pyc)
    app = api()
    app.run(host='0.0.0.0', port=5000, debug=True)
