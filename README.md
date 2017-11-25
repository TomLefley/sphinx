# Sphinx
> A RESTful question and answer engine written in Python with Flask

Sphinx was built as a tool for use in coding challenge type scenarios. The app starts up with several 'riddles' loaded and can accept more via its API.

A riddle consists of a description and generated question. Consumers ask for a new question from a riddle and have one chance to respond with the correct answer.

## Installation

Because Sphinx dynamically loads and runs unchecked code it is _highly_ recommended to run it within docker.

* `build.sh` will create the required docker image
* `sphinx.sh` will start up Sphinx in docker once the required image has been built

## Usage

Sphinx has the following REST API:
* `GET` `/` Returns this README file
* `GET` `/riddles` Lists all available riddle names
* `GET` `/<riddle>/description` Returns a short description of how to answer the riddle
* `GET` `/<riddle>/question` Generates and returns a new question from the riddle. Sets the `X-Question-Id` header for the answer.
* `POST` `/<riddle>/answer` Submit and answer for the question generated. Set the `X-Question-Id` header with the id given by the question call. The request body should be `application/json` of the form `{ "answer": "..." }`
* `POST` `/<riddle>/upload` Upload a new riddle file as plaintext Python

Riddles should be written in Python and define the following methods:
* `description()` should return a string description of the riddle
* `question()` should return a tuple of ``(question: string, answer: string)``

Any riddles present in `/riddles` when the docker image is built will be loaded at startup.
