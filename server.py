import os
import logging
from flask import Flask, jsonify, request
from flask import send_file
from flask_cors import CORS
from config import CONVERTED_DIR
app = Flask(__name__)
app.config.from_mapping(os.environ)
from tools import *

CORS(app)

logging.basicConfig(level=logging.DEBUG ,format='%(levelname)s:%(message)s')

@app.route('/api/document' , methods=['POST'])
def replace():

    if 'hash' in request.args:
        hash = request.args.get('hash')
        logging.debug('Hash is %s'%hash)
        r = Manager(hash)
        try:
            r.download_ipfs_document()
            r.replace(request.json)
            r.doc_pdf()

            return send_file('%s/%s.pdf'%(CONVERTED_DIR,hash), as_attachment=True), 200

        except FileNotFoundError as e:
            return jsonify({"code": 500, "message": str(e)}), 500
        except Exception as e:
            return jsonify({"code": 500, "message": str(e)}), 500

@app.errorhandler(403)
def forbidden(ex):
    return jsonify({"code": 403, "message": ex.description}), 403


@app.errorhandler(404)
def not_found(ex):
    return jsonify({"code": 404, "message": ex.description}), 404

if __name__ == '__main__':
    app.run(debug=True)
