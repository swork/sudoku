from wsgiref.validate import validator
from wsgiref.simple_server import make_server
from renlabs.sudoku.api import application
import logging
logging.basicConfig()
logger=logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# This is the application wrapped in a validator
validator_app = validator(application)

httpd = make_server('', 8000, validator_app)
print("Listening on port 8000....")
httpd.serve_forever()
