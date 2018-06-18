import flask
from flask import request, jsonify
import sqlite3
from html_parser import get_schedule
import sys

app = flask.Flask(__name__)
app.config["DEBUG"] = True

all_universities_list = [{
                             'id': 0,
                             'name': 'Lviv Polytechnic National University',
                             'image': 'http://lpnu.ua/sites/all/themes/lpnu/img/logo-md-uk-sprite.png'
                         }, {
                             'id': 1,
                             'name': 'Lviv National University',
                             'image': 'http://www.lnu.edu.ua/wp-content/uploads/2015/01/%D0%B3%D0%B5%D1%80%D0%B1.jpg'
                         }]


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''
        <body style='font-family: "Segoe UI Light";text-align: center;padding: 0;margin-bottom: 0;'>
            <div style='height: 10vh;'></div>
            <h1>University Helper</h1>
            <h3>A prototype API for getting university schedule.</h3>
            <div style='display: inline-block;text-align: left;padding: 10px;'>
                <p><i><a href='/api/universities/all'>/api/universities/all</a></i></p>
                <p><i><a href='/api/nulp/institutes/all'>/api/nulp/institutes/all</a></i></p>
                <p><i><a href='/api/nulp/groups/all'>/api/nulp/groups/all</a></i></p>
                <p><i><a href='/api/nulp/groups?institute_id=9'>/api/nulp/groups?institute_id=9</a></i></p>
                <p><i><a href='/api/nulp/schedule?institute_id=9&group_id=10982'>/api/nulp/schedule?institute_id=9&group_id=10982</a></i></p>
            </div>
            <div style='display: inline-block;text-align: left;padding: 10px;'>
                <p>all universities</p>
                <p>all institutes of nulp</p>
                <p>all groups of nulp</p>
                <p>all groups of some institute</p>
                <p>schedule for some group</p>
            </div>
        </body>
        '''


@app.route('/api/universities/all', methods=['GET'])
def api_all_universities():
    return jsonify(all_universities_list)


@app.route('/api/nulp/institutes/all', methods=['GET'])
def api_nulp_institutes():
    
    connection = sqlite3.connect('nulp.db')
    connection.row_factory = dict_factory
    cur = connection.cursor()
    
    institutes = cur.execute('SELECT * FROM institutes;').fetchall()
    
    return jsonify(institutes)


@app.route('/api/nulp/groups/all', methods=['GET'])
def api_nulp_allgroups():
    
    connection = sqlite3.connect('nulp.db')
    connection.row_factory = dict_factory
    cur = connection.cursor()
    
    groups = cur.execute('SELECT * FROM groups;').fetchall()
    
    return jsonify(groups)


@app.route('/api/nulp/groups', methods=['GET'])
def api_nulp_groups():
    
    query_parameters = request.args
    institute_id = query_parameters.get('institute_id')

    if not (institute_id):
        return page_not_found(404)
    
    connection = sqlite3.connect('nulp.db')
    connection.row_factory = dict_factory
    cur = connection.cursor()

    groups = cur.execute('SELECT * FROM groups WHERE institute_id=?;', institute_id).fetchall()

    return jsonify(groups)


@app.route('/api/nulp/schedule', methods=['GET'])
def api_nulp_schedule():
    
    query_parameters = request.args
    institute_id = query_parameters.get('institute_id')
    group_id = query_parameters.get('group_id')
    
    return jsonify(get_schedule(institute_id, group_id))


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

app.run()
