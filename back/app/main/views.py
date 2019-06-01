import json
import pandas as pd
from . import main
from datetime import datetime
from flask import render_template, session, redirect, url_for, request, send_from_directory, jsonify, flash, request
from .. import mongo

@main.route('/', methods=['GET','POST'])
def index():
    return 'hello,world'

@main.route('/log', methods=['GET','POST'])
def test():
    devices = list(mongo.db.devices.find({},{'_id':0}))
    now = datetime.now()
    for i,v  in enumerate(mongo.db.devices.find({}, {'_id':0})):
        if mongo.db.check_log.find_one({'id': v['id'],'date':{'$gt': datetime(now.year, now.month, now.day)}}):
            devices[i]['isCheck'] = True
            devices[i]['date'] = mongo.db.check_log.find_one({'id': v['id'],'date':{'$gt': datetime(now.year, now.month, now.day)}})['date'].strftime('%H:%M')
        else:
            devices[i]['isCheck'] = False
            devices[i]['date'] = '待检查'
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
    df = pd.DataFrame(list(db.check_log.find()))
    df['date2'] = df.date.apply(lambda x: x.date())
    df = df.pivot_table(index='date2', columns='user', values='id', aggfunc='count')
    return jsonify({'index': df.index.tolist(), 'columns': df.columns.tolist(), 'table': df.to_dict('records')})