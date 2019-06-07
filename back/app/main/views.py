import json
import pandas as pd
from . import main
from datetime import datetime
from flask import render_template, session, redirect, url_for, request, send_from_directory, jsonify, flash, request
from .. import mongo
from bson import ObjectId

@main.route('/', methods=['GET','POST'])
def index():
    return 'hello,world'

@main.route('/log', methods=['GET','POST'])
def test():
    devices = list(mongo.db.devices.find({}))
    now = datetime.now()
    for i,v  in enumerate(devices):
        if mongo.db.check_log.find_one({'id': v['_id'],'date':{'$gt': datetime(now.year, now.month, now.day)}}):
            devices[i]['isCheck'] = True
            devices[i]['check_date'] = mongo.db.check_log.find_one({'id': v['_id'],'date':{'$gt': datetime(now.year, now.month, now.day)}})['date'].strftime('%H:%M')
        else:
            devices[i]['isCheck'] = False
            devices[i]['check_date'] = '待检查'
    return jsonify({'data': devices})

@main.route('/check', methods=['POST'])
def check():
    params = json.loads(request.data.decode('utf-8'))
    print(params)
    id = params['id']
    mongo.db.check_log.insert_one({'id': int(id), 'date': datetime.now(), 'user': 'ww'})
    return jsonify({'message': 'ok'})

@main.route('/check_collect')
def check_collect():
    params = json.loads(request.data.decode('utf-8'))
    df = pd.DataFrame(list(mongo.db.check_log.find()))
    df['date2'] = df.date.apply(lambda x: x.date())
    df = df.pivot_table(index='date2', columns='user', values='id', aggfunc='count')
    return jsonify({'index': df.index.tolist(), 'columns': df.columns.tolist(), 'table': df.to_dict('records')})

@main.route('/devices', methods=['GET', 'PUT', 'DELETE', 'UPDATE'])
def devices():
    if request.method == 'GET':
        devices = list(mongo.db.devices.find())
        return jsonify({'data': devices})
    if request.method == 'DELETE':
        _id = request.args.get('_id')
        oid = ObjectId(_id)
        mongo.db.devices.delete_one({'_id': oid})
        return '删除成功'
    if request.method == "PUT":
        mongo.db.devices.insert_one(request.json)
        return '添加成功'