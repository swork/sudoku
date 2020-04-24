import flask
from flask.views import MethodView
from . import Sudoku
from textwrap import wrap, dedent

import logging, os, json
logger = logging.getLogger(__name__)
logger.setLevel(int(os.environ.get('LEVEL', logging.DEBUG)))

application = flask.Flask('sudoku')  # __name__.split('.',1)[0])  # "sudoku"

class SudokuAPI(MethodView):
    def get(self, puzzle_json):
        """puzzle_json: JSON string, a list of nine rows of nine integers"""
        a = flask.request.args
        if puzzle_json is None:
            rows_str = a.get('rows') or a.get('row') or a.get('r')
            if rows_str:
                return self.solve(rows_str)
            else:
                return flask.jsonify(
                    status=200,
                    message='OK',
                    body = {
                        "sudoku": "welcome",
                        "info": wrap(
                            dedent("""\
                            Give a JSON list of nine lists of integers, each a
                            row of a sudoku puzzle, with zeros for the empty
                            cells. Get back a solution, maybe one of several.
                            POST or PUT JSON, or set query parameter rows or r
                            to JSON-decodable string, or just append that
                            string to the URL path."""),
                            drop_whitespace=True)})
        # else
        return self.solve(puzzle_json)

    def post(self):
        r = flask.request
        if r.content_length < 1000 * 1000:
            body_str = flask.request.get_data()
            return self.solve(body_str)

    def put(self):
        body_str = flask.request.get_data()
        return self.solve(body_str)

    def solve(self, input):
        s = Sudoku()
        logger.debug(f'solve:input:{input!r}')
        try:
            while isinstance(input, str) or isinstance(input, bytes):
                input = json.loads(input)
        except json.decoder.JSONDecodeError:
            return self.bomb(f"Couldn't decode string as json: {input!r}")
        if not isinstance(input, list):
            return self.bomb(f"Decoded to invalid input: {input!r}")
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

    def bomb(self, message):
        return flask.jsonify(
            status=400,
            message="Error",
            body={
                "message": message
            })

sudoku_view = SudokuAPI.as_view('sudoku_api')
application.add_url_rule('/', defaults={'puzzle_json': None},
                         view_func=sudoku_view, methods=['GET'])
application.add_url_rule('/', view_func=sudoku_view, methods=['POST', 'PUT'])
application.add_url_rule('/<puzzle_json>', view_func=sudoku_view, methods=['GET'])
