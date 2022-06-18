import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from flask import Blueprint, Flask, request, jsonify
import pandas as pd
import json
import random
from extra_data import region_list, reply_main

r_list_1 = region_list.region_list_1
r_list_2 = region_list.region_list_2
region_eng = region_list.region_eng

big_reply = reply_main.big_reply

thumbnail = pd.read_csv("./data/region_data/thumbnail/Thumbnail.csv")

thumbnail_arr = []

for i in range(10) :
    thumbnail_arr.append(thumbnail.iloc[i]['thumbnail'])


show_lease = Blueprint("show_lease", __name__, url_prefix='/show_lease')

@show_lease.route("/")
def show_lease_home():
    return "show_lease"

@show_lease.route("/region_list_1", methods=['GET', 'POST'])
def show_region_list_1():
    
    body = request.get_json()
    
    page_type = body['action']['clientExtra']['page_type']
    
    # ----------------------------------------------
    res = {
    "version": "2.0",
    "template": {
        "outputs": []
        }}
    
    tmp_quickReplies_set = {"quickReplies": []}
    # ----------------------------------------------
    
    r_text = ""
    
    if page_type == 'before':
        input_list = r_list_1
        
    elif page_type == 'next':
        input_list = r_list_2
    
    else:
        pass
    
    for i in range(len(input_list)):
        r_text = str(r_text + input_list[i] + '\n')
    
    if page_type == 'before':
        res['template']['outputs'].append({"simpleText": {"text": "원하시는 지역을 선택하세요." + '\n\n'
                                                      + r_text + '\n(다음 페이지)'}})
        
    elif page_type == 'next':
        res['template']['outputs'].append({"simpleText": {"text": "원하시는 지역을 선택하세요." + '\n\n'
                                                      + r_text + '\n(이전 페이지)'}})
        
    else:
        pass
    
    for i in range(len(input_list)):
        tmp_quickReplies_set['quickReplies'].append({"label": input_list[i] , "action": "block", 
                                                     "blockId": "62986945e7a0253c7662d9c7", "extra": {"region_type" : input_list[i]}})
    
    if page_type == 'before':
        tmp_quickReplies_set['quickReplies'].append({"label": "다음 페이지" , "action": "block", 
                                                     "blockId": "629854f6f591aa190554aa9c", "extra": {"page_type" : "next"}})
    elif page_type == 'next':
        tmp_quickReplies_set['quickReplies'].append({"label": "이전 페이지" , "action": "block", 
                                                     "blockId": "629854f6f591aa190554aa9c", "extra": {"page_type" : "before"}})
    else:
        pass
    
    res['template'].update(tmp_quickReplies_set)
    
    return jsonify(res)

@show_lease.route("/lease_list", methods=['GET', 'POST'])
def show_lease_list():
    
    body = request.get_json()
    
    region_type = body['action']['clientExtra']['region_type']
    
    # ----------------------------------------------
    res= {
    "version": "2.0",
    "template": {
        "outputs": [{
            "carousel" :{
                "type": "basicCard",
                "items": []
            }
        }]
        }}
    
    tmp_quickReplies_set = {"quickReplies": []}
    # ----------------------------------------------
    #-----------------------------------------------
    region_notice = pd.read_csv("./data/region_data/"+ region_eng[region_type] + "_notice.csv")
    region_url = pd.read_csv("./data/region_data/"+ region_eng[region_type] + "_url.csv")
    
    r_des = []
    
    rand_thumb = random.sample(thumbnail_arr, 10)
    
    
    for i in range(len(region_notice)):
        r_des.append(region_notice.iloc[i]['name'] 
                     + '\n공급유형 : ' + region_notice.iloc[i]['title'] 
                     + '\n공고일자 : ' + region_notice.iloc[i]['re_date'])
      
    for i in range(len(r_des)):
        res['template']['outputs'][0]['carousel']['items'].append({
                        "description": r_des[i],
                        "thumbnail": {
                            "imageUrl": rand_thumb[i]
                        },
                        "buttons": [
                            {
                                "action":  "webLink",
                                "label": "자세히 보기",
                                "webLinkUrl": region_url.iloc[i]['url']
                            }
                        ]
                    })
  
    tmp_quickReplies_set['quickReplies'].append({"label": "지역 목록으로" , "action": "block", 
                                                     "blockId": "629854f6f591aa190554aa9c", "extra": {"page_type" : "before"}})
    tmp_quickReplies_set['quickReplies'].append({"label": "메인메뉴" , "action": "block", 
                                                     "blockId": big_reply['메인메뉴']})
    
    res['template'].update(tmp_quickReplies_set)
    
    return jsonify(res)