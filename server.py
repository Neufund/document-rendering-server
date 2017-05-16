import os ,sys
import logging
from classes.exceptions import *
from flask import Flask, jsonify, request , abort
from flask import send_file
from flask_cors import CORS

from classes.documents import *
app = Flask(__name__)

app.config.from_pyfile('config.py')
app.config.from_mapping(os.environ)

def init_logging():
    """Initializes logging."""
    if LOG_COLOR:
        logging.addLevelName(logging.DEBUG,
                             "\033[1;00m%s\033[1;0m" % logging.getLevelName(logging.DEBUG))
        logging.addLevelName(logging.INFO,
                             "\033[1;34m%s\033[1;0m" % logging.getLevelName(logging.INFO))
        logging.addLevelName(logging.WARNING,
                             "\033[0;33m%s\033[0;0m" % logging.getLevelName(logging.WARNING))
        logging.addLevelName(logging.ERROR,
                             "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.ERROR))
        logging.addLevelName(logging.CRITICAL,
                             "\033[0;31m%s\033[0;0m" % logging.getLevelName(logging.CRITICAL))

    logging.basicConfig(level=LOG_LEVEL,
                        format=LOG_FORMAT, style='{')

def _log_exception():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    logging.error("Exception type#{}#{}#{}".format(
        exc_type, file_name, exc_tb.tb_lineno))


@app.route('/api/document' , methods=['POST'])
def replace():
    required = ['hash' , 'type']
    if len(request.args) != len(required):
        abort(400 , {'message': 'invalid arguments'})

    for r in required:
        if r not in request.args:
            abort(400, {'message': '%s argument is not missing'})

    for r in request.args:
        if r not in required:
            abort(400 , {'message': '%s argument is not required'})

    if request.args['type'] not in list(SUPPORTED_FILE.values()):
        abort(400, {'message': 'Type should be one of following [ %s ]'%', '.join(list(SUPPORTED_FILE.values()))})

    hash = request.args['hash']
    type = request.args['type']
    logging.debug('Hash is %s'%hash)

    dic = request.json if request.json else {}

    pdf_object = PdfFactory.factory(type)(hash, dic)

    pdf_file = '%s/%s.pdf'%(CONVERTED_DIR, pdf_object.encoded_hash)

    if not os.path.isfile(pdf_file):
        pdf_object.generate()

    return send_file(pdf_file, as_attachment=True), 200


@app.errorhandler(403)
def forbidden(ex):
    _log_exception()
    return jsonify({"code": 403, "message": ex.description}), 403

@app.errorhandler(400)
def forbidden(ex):
    _log_exception()
    return jsonify({"code": 400, "message": ex.description}), 400


@app.errorhandler(404)
def not_found(ex):
    _log_exception()
    return jsonify({"code": 404, "message": ex.description}), 404

@app.errorhandler(405)
def not_found(ex):
    _log_exception()
    return jsonify({"code": 405, "message": ex.description}), 405

@app.errorhandler(500)
def internal_server_error(ex):
    logging.error('Server Error: %s', ex.description)
    return jsonify({"code": 404, "message": ex.description}), 500


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    message = str(e)
    if isinstance(e, MainException):
        code = e.get_code()
        message = e.get_message()

    _log_exception()
    return jsonify({"code": code, "message": message}),code


if __name__ == '__main__':
    app.config.from_mapping(os.environ)
    CORS(app)
    init_logging()
    app.run(debug=True)
