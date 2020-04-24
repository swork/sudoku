import flask
from . import Sudoku
from textwrap import wrap, dedent

import logging, os
logger = logging.getLogger(__name__)
logger.setLevel(int(os.environ.get('LEVEL', logging.DEBUG)))

application = flask.Flask('sudoku')  # __name__.split('.',1)[0])  # "sudoku"

@application.route('/', methods=['GET'])
def inform():
    return flask.jsonify(
        status=200,
        message='OK',
        body = {
            "sudoku": "welcome",
            "info": wrap(
                dedent("""\
                Post a JSON list of nine lists of integers,
                each a row of a sudoku puzzle,
                with zeros for the empty squares.
                Get back a solution, maybe one of several."""),
                drop_whitespace=True)})

@application.route('/', methods=['POST'])
def solve():
    s = Sudoku()
    input = flask.request.get_json(force=True)
    logger.debug(f'input:{input}')
    s.inputList(input)
    if s.solution:
        return flask.jsonify(
            status=200,
            message='OK',
            body={
                "input": input,
                "solution": s.solution})
    return flask.jsonify(
        status=204,
        message='No solution',
        body={
            "input": input,
            "nosolution": "No solution is possible."
        })

