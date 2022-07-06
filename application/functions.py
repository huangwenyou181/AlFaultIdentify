from msilib.schema import tables
import time, json, copy
from unicodedata import name

from flask import redirect
from numpy import alen, var
from application.models import Image, Result, Class, User

import os

testJson = {
    "len": 2,
    "result": [
        {
            "class_id": 1,
            "score": 0.888,
            "x_min": 50,
            "x_max": 100,
            "y_min": 50,
            "y_max": 10
        },
        {
            "class_id": 2,
            "score": 0.999,
            "x_min": 150,
            "x_max": 200,
            "y_min": 150,
            "y_max": 20
        }
    ]
}
def change_type(byte):    
    if isinstance(byte,bytes):
        return str(byte,encoding="utf-8")  
    return json.JSONEncoder.default(byte)

def generateTimeName():
    timeStamp = int(time.time())
    timeArray = time.localtime(timeStamp)
    styleTime = time.strftime("%Y_%m_%d_%H_%M_%S", timeArray)
    return styleTime

def dbAddImage(imageName, database, savePath, user):
    image = Image(imagename = imageName, path = savePath, userid = user)
    database.session.add(image)
    database.session.commit()
    return image.id
    
def process(imageId, database):
    path = Image.query.get_or_404(int(imageId)).path
    
    # print(path)
    # print(1)
    tp ='python ./application/PaddleDetection/deploy/python/infer.py --model_dir=./application/PaddleDetection/output_export/yolov3_darknet_voc/ --output_dir=./application/static/images/output --image_file=./application'+path
    f = os.popen(tp)
    data = "nofound"
    data = f.readlines()
    # print(data)
    # print(type(data))
    f.close()
    path_data = data[-1]
    a = path_data.find('save result to: ./application/static/images/output\\')
    length1 = len('save result to: ./application/static/images/output\\')
    # print(path_data[(a+length1):-1])
    path = '/static/images/output/' + path_data[(a+length1):-1]
    # print(path)

    length = len(data)
    class_id = []
    score = []
    for i in range(length):
        j = 0
        string = data[i]
        # print(string)
        if(string.find('class_id:') != -1):
            # print(1)

            a = string.find('class_id:')
            length1 = len('class_id:')
            b = string.find(', confidence:')
            class_id.append(1)
            class_id[j] = string[(a + length1):b]
            class_id.append(1)
            class_id[j] = int(class_id[j])
            
            length2 = len(', confidence:')
            c = string.find(',left_top:[')
            score.append(1)
            score[j] = string[(b + length2):c]
            score.append(1)
            score[j] = float(score[j])

            j = j + 1
            length = j

            # length3 = len(',left_top:[')
            # d = string.find('], right_bottom:[')
            # temp.append(1)
            # temp[j] = string[(c + length3):d]
            # strlist = temp[j].split(',')
            # print(strlist[0])

            # length4 = len(', y=')
            # e = string.find(', width=')
            # ymin.append(1)
            # ymin[i] = string[(d + length4):e]
            # ymin.append(1)
            # ymin[i] = int(ymin[i])

            # length5 = len(', width=')
            # f = string.find(', height=')
            # width = string[(e + length5):f]
            # width = int(width)

            # length6 = len(', height=')
            # height = string[(f + length6):]
            # height = int(height)
            # xmax.append(1)
            # xmax[i] = xmin[i] + width
            # ymax.append(1)
            # ymax[i] = ymin[i] + height
        

    dict = {}
    dict['len'] = length
    dict['result'] = []
    a = dict['result']
    for i in range(length):
        a.append(1)
        a[i] = {}
        a[i]['class_id'] = class_id[i]
        a[i]['score'] = score[i]



    reJson = copy.deepcopy(dict)
    reJson["imageSrc"] = path
    for re in reJson["result"]:
        result = Result(
            imageid = imageId,
            classid = re["class_id"],
            score = re["score"],
        )
        database.session.add(result)
        classid = re["class_id"] + 1
        re["class_name"] = Class.query.get_or_404(classid).classname
        re["description"] = Class.query.get_or_404(classid).classtext
    database.session.commit()
    return json.dumps(reJson)

def detailReTab(userid, database):
    
    queryid = [userid]
    if(userid == 1):
        queryid = database.session.query(User.id)
    
    results = []
    images = database.session.query(Image.id, Image.path, Image.userid).filter(Image.userid.in_(queryid))
    tableData = [0, 0, 0, 0]
    for img in images:
        imgResult = {}
        reQuery = database.session.query(Result.classid, Result.min_x, Result.max_x, Result.min_y, Result.max_y).filter(Result.id == img[0])
        imgResult["len"] = reQuery.count()
        imgResult["src"] = img[1]
        imgResult["user"] = database.session.query(User.name).filter(User.id == img[2]).first()[0]
        result = []
        for re in reQuery:
            tableData[re[0] - 1] += 1
            reObj = {}
            reObj["class_name"] = Class.query.get_or_404(re[0]).classname
            reObj["min_x"] = re[1]
            reObj["max_x"] = re[2]
            reObj["min_y"] = re[3]
            reObj["max_y"] = re[4]
            result.append(reObj)
        imgResult["result"] = copy.deepcopy(result)
        results.append(imgResult)
    
    length = len(results)
    reTab = {}
    reTab["length"] = length
    reTab["results"] = results
    reTab["data"] = tableData
    
    return reTab
    
    
def getUserList(userid, database):
    queryid = [userid]
    if(userid == 1):
        queryid = database.session.query(User.id)
    
    names = database.session.query(User.name).filter(User.id.in_(queryid)).all()
    namelist = []
    for i in names:
        namelist.append(i[0])
    
    return {'namelist': namelist}

def getDataAndDate(uname, database):
    names = []
    if(uname == "Select ALL"):
        names = database.session.query(User.id).all()
    else:
        names = database.session.query(User.id).filter(User.name == uname)
    uid = []
    for i in names:
        uid.append(i[0])
    
    dateDict = {}
    images = database.session.query(Image.imagename, Image.id).filter(Image.userid.in_(uid))
    for i in images:
        date = i[0]
        dateArr = date.split('_')
        dateStr = dateArr[0] + '/' + dateArr[1] + '/' + dateArr[2]
        dateDict.setdefault(dateStr, [0, 0, 0, 0])
        results = database.session.query(Result.classid).filter(Result.imageid == i[1])
        for re in results:
            dateDict[dateStr][re[0] - 1] += 1
        
   
    reDict = {} 
    reDict['date'] = list(dateDict.keys())
    reDict["data"] = [[], [], [], []]
    tempList = list(dateDict.values())
    for i in tempList:
        reDict["data"][0].append(i[0])
        reDict["data"][1].append(i[1])
        reDict["data"][2].append(i[2])
        reDict["data"][3].append(i[3])
    return reDict

    
    