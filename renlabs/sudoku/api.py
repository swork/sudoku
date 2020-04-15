import flask
from . import Sudoku
from textwrap import wrap, dedent

application = flask.Flask('sudoKu')  # __name__.split('.',1)[0])  # "sudoku"

@application.route('/sudoku', methods=['GET', 'POST'])
def index_solve():
    if flask.request.method == 'GET':
        return flask.jsonify(
            status=200,
            message='OK',
            body = {
                "sudoku": "welcome",
                "info": wrap(dedent("""\
                    Post a JSON list of nine lists of integers,
                    each a row of a sudoku puzzle,
                    with zeros for the empty squares.
                    Get back a solution, maybe one of several."""),
                             drop_whitespace=True)})
    elif flask.request.method == 'POST':
        s = Sudoku()
        input = flask.request.get_json(force=True)
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

