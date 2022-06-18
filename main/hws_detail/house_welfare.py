import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from flask import Blueprint, Flask, request, jsonify
import pandas as pd
from extra_data import dict_code, url_list, reply_main

# ------------------------------------------------------------------------------------------------------
service_code = dict_code.service_code
big_reply = reply_main.big_reply

URL = url_list.URL
# ------------------------------------------------------------------------------------------------------
# ----- house_welfare blueprint set ----------------------------------------------------------------------------
blue_house_welfare = Blueprint("house_welfare", __name__, url_prefix='/house_welfare')
#---------------------------------------------------------------------------------------------------------------

# ----- house_welfare root -------------------------------------------------------------------------------------
@blue_house_welfare.route("/")
def house_welfare_home():
    return "house_welfare"
# --------------------------------------------------------------------------------------------------------------

# ----- house_welfare/info_des ---------------------------------------------------------------------------------
@blue_house_welfare.route("/info_des", methods=['POST'])
def house_welfare_info_des():
    body = request.get_json()
    
    welfare_info_house = pd.read_csv("./data/welfare_info/housing_welfare_service.csv")
    
    welfare_dict = {'통합공공임대주택' : 0, '영구임대주택' : 1, '행복주택': 2, 
                    '전세임대주택': 3, '매입임대주택' : 4, '국민임대주택' : 5, 
                    '공공지원민간임대주택' : 6, '주거복지동주택': 7, '공공기숙사' : 8, 
                    '장기전세주택' : 9, '공공임대주택':10}
    
    welfare_type = body['action']['clientExtra']['welfare_type']
    

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": str(welfare_info_house.iloc[welfare_dict[welfare_type]]['title']) + "\n\n" 
                                + str(welfare_info_house.iloc[welfare_dict[welfare_type]]['describe'])
                    }
                }
            ],
            "quickReplies": [
                {
                "label": "상세정보",
                "action": "block",
                "blockId": big_reply['상세정보'],
                "extra": {"welfare_type" : welfare_type}
                },
                {
                "label": "주택복지",
                "action": "block",
                "blockId": big_reply['주택복지']
                },
                {
                "label": "메인메뉴",
                "action": "block",
                "blockId": big_reply['메인메뉴']
                }
            ]
        }
    }

    return responseBody
# --------------------------------------------------------------------------------------------------------------

# ----- house_welfare/info -------------------------------------------------------------------------------------
@blue_house_welfare.route("/info", methods=['GET', 'POST'])
def housing_welfare():
    req = request.get_json()
    
    welfare_info_house = pd.read_csv("./data/welfare_info/housing_welfare_service.csv")
    
    # ----------------------------------------------
    res = {
    "version": "2.0",
    "template": {
        "outputs": [{
            "carousel" :{
                "type": "itemCard",
                "items": []
            }
        }]
        }}
    
    tmp_quickReplies_set = {"quickReplies": []}
    # ----------------------------------------------
    
    for i in range(len(welfare_info_house)):
        if welfare_info_house.iloc[i]['title'] == '매입임대주택':
            continue
        elif welfare_info_house.iloc[i]['title'] == '전세임대주택':
            res['template']['outputs'][0]['carousel']['items'].append({
              "imageTitle": {
                "title": welfare_info_house.iloc[i]['title'],
                "imageUrl" : ""
              },
              "itemList": [
                {
                  "title": "설명",
                  "description": welfare_info_house.iloc[i]['describe']
                },
                {
                  "title": "임대기간",
                  "description": welfare_info_house.iloc[i]['term']
                },
                {
                  "title" : "전용면적",
                  "description" : welfare_info_house.iloc[i]['dedicated_area']
                },
                {
                  "title" : "지원한도",
                  "description" : welfare_info_house.iloc[i]['condition']
                }
              ],
              "itemListAlignment": "left",
              "buttons": [
                {
                  "label": "설명 보기",
                  "action": "block",
                  "blockId" : big_reply['설명보기'],
                  "extra": {"welfare_type" : welfare_info_house.iloc[i]['title']}
                },
                {
                  "label": "링크 연결",
                  "action": "webLink",
                  "webLinkUrl": URL + service_code[welfare_info_house.iloc[i]['title']]
                }
              ]
            })
        else:
            res['template']['outputs'][0]['carousel']['items'].append({
              "imageTitle": {
                "title": welfare_info_house.iloc[i]['title'],
                "imageUrl" : ""
              },
              "itemList": [
                {
                  "title": "설명",
                  "description": welfare_info_house.iloc[i]['describe']
                },
                {
                  "title": "임대기간",
                  "description": welfare_info_house.iloc[i]['term']
                },
                {
                  "title" : "전용면적",
                  "description" : welfare_info_house.iloc[i]['dedicated_area']
                },
                {
                  "title" : "임대조건",
                  "description" : welfare_info_house.iloc[i]['condition']
                }
              ],
              "itemListAlignment": "left",
              "buttons": [
                {
                  "label": "설명 보기",
                  "action": "block",
                  "blockId" : big_reply['설명보기'],
                  "extra": {"welfare_type" : welfare_info_house.iloc[i]['title']}
                },
                {
                  "label": "링크 연결",
                  "action": "webLink",
                  "webLinkUrl": URL + service_code[welfare_info_house.iloc[i]['title']]
                }
              ]
            })
    

    tmp_quickReplies_set['quickReplies'].append({
        "action": "block",
        "blockId": big_reply['메인메뉴'],
        "label": "메인메뉴"
      })
    
    res['template'].update(tmp_quickReplies_set)
    
    #답변 전송
    return jsonify(res)
# --------------------------------------------------------------------------------------------------------------