import os
import logging
from werkzeug.exceptions import HTTPException
from flask import Flask, jsonify, request , abort
from flask import send_file
from flask_cors import CORS
from config import *
from tools import *


app = Flask(__name__)
app.config.from_mapping(os.environ)

CORS(app)

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


init_logging()

@app.route('/api/document' , methods=['POST'])
def replace():

    if 'hash' in request.args:
        hash = request.args.get('hash')
        logging.debug('Hash is %s'%hash)
        r = Manager(hash)

        r.download_ipfs_document()
        r.replace(request.json)
        r.doc_pdf()

        return send_file('%s/%s.pdf'%(CONVERTED_DIR,hash), as_attachment=True), 200
    else:
        abort(400)

@app.errorhandler(403)
def forbidden(ex):
    logging.error('Server Error: %s', ex.description)
    return jsonify({"code": 403, "message": ex.description}), 403

@app.errorhandler(400)
def forbidden(ex):
    logging.error('Server Error: %s', ex.description)
    return jsonify({"code": 400, "message": ex.description}), 400


@app.errorhandler(404)
def not_found(ex):
    logging.error('Server Error: %s', ex.description)
    return jsonify({"code": 404, "message": ex.description}), 404

@app.errorhandler(405)
def not_found(ex):
    logging.error('Server Error: %s', ex.description)
    return jsonify({"code": 405, "message": ex.description}), 405

@app.errorhandler(500)
def internal_server_error(ex):
    logging.error('Server Error: %s', ex.description)
    return jsonify({"code": 404, "message": ex.description}), 500


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    message =''
    if isinstance(e, FileNotFoundError):
        code = 404
        message = str(e)
    elif isinstance(e, FileExistsError):
        message = str(e)
        code = 403
    elif isinstance(e, IOError):
        message = str(e)
        code = 500
    elif isinstance(e, HTTPException):
        message = e.description
        code = e.code

    logging.error('Server Error: %s', message)
    return jsonify({"code": code, "message": message}),code


if __name__ == '__main__':
    app.run(debug=True)
