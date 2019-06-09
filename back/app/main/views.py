import json
import pandas as pd
from . import main
from datetime import datetime, timedelta
from dateutil import parser, tz
import calendar
from flask import render_template, session, redirect, url_for, request, send_from_directory, jsonify, flash, request, g
from .. import mongo
from app.auth.auth import multi_auth
from app.common import RESULT
from bson import ObjectId

@main.route('/', methods=['GET','POST'])
def index():
    return 'hello,world'

@main.route('/log', methods=['GET','POST'])
@multi_auth.login_required
def log():
    devices = list(mongo.db.devices.find({}))
    now = datetime.now()
    for i,v  in enumerate(devices):
        check_log = mongo.db.check_log.find_one({'device_id': ObjectId(v['_id']),'date':{'$gt': datetime(now.year, now.month, now.day)}})
        if check_log:
            devices[i]['isCheck'] = True
            devices[i]['check_date'] = check_log['date'].strftime('%H:%M')
            devices[i]['result'] = RESULT[check_log['result']]
        else:
            devices[i]['isCheck'] = False
            devices[i]['check_date'] = ''
            devices[i]['result'] = '待检查'
    return jsonify({'data': devices})

@main.route('/checklog', methods=['GET'])
@multi_auth.login_required
def checklog():
    print(request.args)
    query = {}
    if request.args.get('result'):
        query['result'] = int(request.args.get('result'))
    if request.args.get('device'):
        query['device_id'] = ObjectId(request.args.get('device'))
    if request.args.get('date') != '':
        date = parser.parse(request.args.get('date')).astimezone(tz.tzlocal())
        date2 = date  + timedelta(days=1)
        query['date'] = {'$gte': datetime(date.year, date.month, date.day), '$lt': datetime(date2.year, date2.month, date2.day)}
    print(query)
    checklog = list(mongo.db.check_log.find(query))
    for i in checklog:
        i['device_name'] = mongo.db.devices.find_one({'_id': ObjectId(i['device_id'])})['name']
        i['result'] = RESULT[i['result']]
    return jsonify({'data': checklog})

@main.route('/check', methods=['POST'])
@multi_auth.login_required
def check():
    #params = json.loads(request.data.decode('utf-8'))
    device = mongo.db.devices.find_one({'code': request.json.get('code')})
    if device is None:
        return jsonify({'message': 'no device', 'code': 40000})
    oid = ObjectId(device['_id'])
    mongo.db.check_log.insert_one({'device_id': oid, 'content': request.json.get('content'), 'result': request.json.get('result'), 'date': datetime.now(), 'user': g.user})
    return jsonify({'message': 'ok'})

@main.route('/check_collect')
def check_collect():
    params = json.loads(request.data.decode('utf-8'))
    df = pd.DataFrame(list(mongo.db.check_log.find()))
    df['date2'] = df.date.apply(lambda x: x.date())
    df = df.pivot_table(index='date2', columns='user', values='id', aggfunc='count')
    return jsonify({'index': df.index.tolist(), 'columns': df.columns.tolist(), 'table': df.to_dict('records')})

@main.route('/devices', methods=['GET', 'PUT', 'DELETE', 'POST'])
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
        oid = ObjectId(request.json.get('_id'))
        del request.json['_id']
        mongo.db.devices.update_one({'_id': oid}, {'$set': request.json}, upsert=True)
        return '添加成功'

@main.route('/report', methods=['GET'])
def report():
    date = parser.parse(request.args.get('date')).astimezone(tz.tzlocal())
    days = min((datetime.now() - datetime(date.year, date.month, 1)).days, calendar.monthrange(date.year, date.month)[1])
    query = {'date': {'$gte': datetime(date.year, date.month, 1), '$lt': datetime(date.year, date.month, days, 23, 59, 59)}}
    df = pd.DataFrame(list(mongo.db.check_log.find(query))) # 当月检查记录
    df2 = pd.DataFrame(list(mongo.db.devices.find())) # 设备表
    df2.index = df2['_id']
    df['设备名称'] = df['device_id'].apply(lambda x: df2.loc[x, 'name'])
    df2.index = df2.name
    df3 = pd.DataFrame()
    df3['应检次数'] = round((days / df2.period))
    df3['实检次数'] = df['设备名称'].value_counts()
    df3.fillna(0, inplace=True)
    df3['巡检率'] = round(df3['实检次数'] / df3['应检次数'], 3) * 100
    df3['巡检率'] = df3['巡检率'].apply(lambda x: "{}%".format(x))
    df3['name'] = df3.index
    return jsonify({'data': df3.to_dict(orient='records')})