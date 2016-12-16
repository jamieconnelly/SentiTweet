import os
import logging
from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response

app = Flask(__name__)


@app.route('/api', methods=['GET'])
def query_sentiment():
    try:
        term = request.args.getlist('term')
        return jsonify(result=term)

    except Exception as ex:
        app.logger.error(type(ex))
        app.logger.error(ex.args)
        app.logger.error(ex)
        return jsonify(error=str(ex))


if __name__ == '__main__':
    LOG_FORMAT = "'%(asctime)s - %(name)s - %(levelname)s - %(message)s'"
    logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    app.log = logging.getLogger(__name__)
    port = os.environ['FLASK_PORT']
    app.run(host='0.0.0.0', port=int(port), debug=False)
