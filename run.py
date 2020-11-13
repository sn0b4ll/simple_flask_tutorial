import logging
import configparser
import json
import requests

from db.model import Father, Child, session

# Init configparser
config = configparser.ConfigParser()
config.read('test.yml')

# Init logging
logging.basicConfig(filename='example.log', level=logging.DEBUG)

# Some example log lines
logging.info(config['DEFAULT']['DB_CONNECTION_STRING'])
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
logging.error('And non-ASCII stuff, too, like Øresund and Malmö')

from flask import Flask, request, Response
app = Flask(__name__)

@app.route('/')
def dashboard():
    resp = requests.get('http://localhost:5000/father')
    resp = json.loads(resp.text)
    # Do stuff, show nicely
    return json.dumps(resp)

@app.route('/father', methods=['GET', 'POST'])
def father():
    if request.method == 'POST':
        data = request.json
        logging.debug('Received data on /father: {}'.format(data))
        father = Father(data['name'], data['last_name'])
        session.add(father)
        session.commit()
        return Response(status=200)

    else:
        ret = []
        for elem in session.query(Father).all():
            tmp = {}
            tmp['name'] = elem.name
            tmp['last_name'] = elem.last_name
            ret.append(tmp)

        # ret = "{}; {}".format(ret, entry.name)
        return json.dumps(ret)

# father = Father()
# child = Child("Kind", father)

# Create objects
# session.add(father)
# session.commit()
# session.add(child)
# session.commit()

# Show all fathers with all children
# for entry in session.query(Father).all():
#     print(entry.name)
#     for child in entry.childs:
#         print(child.name)

