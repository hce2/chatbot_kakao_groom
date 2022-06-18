import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from flask import Blueprint, Flask, request, jsonify
import pandas as pd
import json
from extra_data import reply_main, dict_code, url_list
# ------------------------------------------------------------------------------------------------------
service_code = dict_code.service_code
reply = reply_main.reply
big_reply = reply_main.big_reply
URL = url_list.URL
# ------------------------------------------------------------------------------------------------------

blue_house_welfare_detail_3 = Blueprint("house_welfare_detail_3", __name__, url_prefix='/house_welfare_detail_3')

@blue_house_welfare_detail_3.route("/")
def house_welfare__detail_3_home():
    return "house_welfare_detail_3"

@blue_house_welfare_detail_3.route("/intro", methods=['GET', 'POST'])
def show_intro():
    body = request.get_json()
    
    welfare_type = body['action']['clientExtra']['welfare_type']
    
    # ----- data url ----------------------------------------------------------------------------
    if welfare_type == '행복주택':
        intro_data = pd.read_csv("./data/house_welfare/happy_house/feature.csv")
        intro_data_1 = pd.read_csv("./data/house_welfare/happy_house/vs_table.csv")
    
    elif welfare_type == '주거복지동주택':
        intro_data = pd.read_csv("./data/house_welfare/dwelling_welfare/intro.csv")
        
    else:
        pass
    # -------------------------------------------------------------------------------------------
    
    # ----------------------------------------------
    res = {
    "version": "2.0",
    "template": {
        "outputs": []
        }}
    
    tmp_quickReplies_set = {"quickReplies": []}
    # ----------------------------------------------
    
    if welfare_type == '행복주택':
        res['template']['outputs'].append({"simpleText": {"text": "■ 특장점" + "\n\t" 
                                                      + "젊음에 희망을! 지역에 활기를! 미래를 위해 행복주택이 있습니다." + "\n\n\t"
                                                      + "♤ " + intro_data.iloc[0]['feature'] + '\n\t' 
                                                          + intro_data.iloc[0]['note'] +'\n\n'
                                                      + "♤ " + intro_data.iloc[1]['feature'] + '\n\t' 
                                                          + intro_data.iloc[1]['note'] +'\n\n'
                                                      + "♤ " + intro_data.iloc[2]['feature'] + '\n\t' 
                                                          + intro_data.iloc[2]['note']  + '\n\n\n'
                                                      
                                                      + "♤ " + intro_data_1.iloc[0]['class'] + '\n\t' 
                                                          + intro_data_1.iloc[0]['happy'] +'\n\n'
                                                      + "♤ " + intro_data_1.iloc[1]['class'] + '\n\t' 
                                                          + intro_data_1.iloc[1]['happy'] +'\n\n'
                                                      + "♤ " + intro_data_1.iloc[2]['class'] + '\n\t' 
                                                          + intro_data_1.iloc[2]['happy']
                                                      }})
    elif welfare_type == '공공지원민간임대주택':
        res['template']['outputs'].append({"basicCard": {
                    "title": "공공지원 민간임대주택 인포그래픽",
                    "thumbnail": {"imageUrl": "https://www.myhome.go.kr/images/portal/myhomeinfo/guideimg/newStay_05.jpg",
                                 "link":{"web" : "https://www.myhome.go.kr/images/portal/myhomeinfo/guideimg/newStay_05.jpg"}}}})
        res['template']['outputs'].append({"basicCard": {
                    "title": "공급계획",
                    "thumbnail": {"imageUrl": "https://www.myhome.go.kr/images/portal/myhomeinfo/guideimg/newStay_06.jpg",
                                 "link":{"web" : "https://www.myhome.go.kr/images/portal/myhomeinfo/guideimg/newStay_06.jpg"}}}})
        
    elif welfare_type == '주거복지동주택':
        res['template']['outputs'].append({"simpleText": {"text": "■ 주거복지동 주택사업 소개" + "\n\n\t" 
                                                      + "♤ " + intro_data.iloc[0]['intro'] + '\n\n\t'
                                                      + "♤ " + intro_data.iloc[1]['intro'] + '\n\n\t' 
                                                      + "♤ " + intro_data.iloc[2]['intro']}})
        res['template']['outputs'].append({"basicCard": {
                    "title": "",
                    "thumbnail": {"imageUrl": "https://www.myhome.go.kr/images/portal/myhomeinfo/guideimg/hwd1_1.jpg",
                                 "link":{"web" : "https://www.myhome.go.kr/images/portal/myhomeinfo/guideimg/hwd1_1.jpg"}}}})
        
        
    res['template']['outputs'].append({"basicCard": {"title": welfare_type + " 링크", "description": "자세한 사항은 링크 연결로...",
                            "thumbnail": {"imageUrl": ""},
                            "buttons": [{
                                        "label": "링크연결",
                                        "action": "webLink",
                                        "webLinkUrl": URL + service_code[welfare_type]}]}})
    
    for i in range(len(reply[welfare_type])):
        tmp_list = list(reply[welfare_type][i].items())
        tmp_quickReplies_set['quickReplies'].append({"label": tmp_list[0][0], "action": "block", 
                                                     "blockId": tmp_list[0][1], "extra": {"welfare_type" : welfare_type}})
        
    tmp_quickReplies_set['quickReplies'].append({"label": "주택복지", "action": "block", 
                                                     "blockId": big_reply['주택복지']})
    tmp_quickReplies_set['quickReplies'].append({"label": "메인메뉴", "action": "block", 
                                                     "blockId": big_reply['메인메뉴']})
    
    res['template'].update(tmp_quickReplies_set)
    
    return jsonify(res)

@blue_house_welfare_detail_3.route("/max_term", methods=['GET', 'POST'])
def show_max_term():
    body = request.get_json()
    
    welfare_type = body['action']['clientExtra']['welfare_type']
    
    # ----- data url ----------------------------------------------------------------------------
    if welfare_type == '행복주택':
        term_data = pd.read_csv("./data/house_welfare/happy_house/max_term.csv")
    # -------------------------------------------------------------------------------------------
    
    # ----------------------------------------------
    res = {
    "version": "2.0",
    "template": {
        "outputs": []
        }}
    
    tmp_quickReplies_set = {"quickReplies": []}
    # ----------------------------------------------
    
    res['template']['outputs'].append({"simpleText": {"text": "■ 최대 거주기간" + "\n\n\t" 
                                                      + "♤ " + term_data.iloc[0]['qualification'] + '\n : \n\t' 
                                                          + term_data.iloc[0]['max_term'] + '\n\n' 
                                                      
                                                      + "♤ " + term_data.iloc[1]['qualification'] + '\n : \n\t' 
                                                          + term_data.iloc[1]['max_term'] + '\n\n' 
                                                      
                                                      + "♤ " + term_data.iloc[2]['qualification'] + '\n : \n\t' 
                                                          + term_data.iloc[2]['max_term']
                                                      }})
    
    res['template']['outputs'].append({"basicCard": {"title": welfare_type + " 링크", "description": "자세한 사항은 링크 연결로...",
                            "thumbnail": {"imageUrl": ""},
                            "buttons": [{
                                        "label": "링크연결",
                                        "action": "webLink",
                                        "webLinkUrl": URL + service_code[welfare_type]}]}})
    
    for i in range(len(reply[welfare_type])):
        tmp_list = list(reply[welfare_type][i].items())
        tmp_quickReplies_set['quickReplies'].append({"label": tmp_list[0][0], "action": "block", 
                                                     "blockId": tmp_list[0][1], "extra": {"welfare_type" : welfare_type}})

    tmp_quickReplies_set['quickReplies'].append({"label": "주택복지", "action": "block", 
                                                     "blockId": big_reply['주택복지']})
    tmp_quickReplies_set['quickReplies'].append({"label": "메인메뉴", "action": "block", 
                                                     "blockId": big_reply['메인메뉴']})
    
    res['template'].update(tmp_quickReplies_set)
        
    return jsonify(res)

@blue_house_welfare_detail_3.route("/detail_info", methods=['GET', 'POST'])
def show_detail_info():
    body = request.get_json()
    
    welfare_type = body['action']['clientExtra']['welfare_type']
    
    # ----- data url ----------------------------------------------------------------------------
    if welfare_type == '공공지원민간임대주택':
        info_data = pd.read_csv("./data/house_welfare/public_support_lease/detail_info.csv")
    # -------------------------------------------------------------------------------------------
    
    # ----------------------------------------------
    res = {
    "version": "2.0",
    "template": {
        "outputs": []
        }}
    
    tmp_quickReplies_set = {"quickReplies": []}
    # ----------------------------------------------
    
    res['template']['outputs'].append({
        "basicCard": {
          "title": "공공지원민간임대주택 상세안내",
          "description": info_data.iloc[4]['site'] + ' : ' +info_data.iloc[4]['address'],
          "thumbnail": {
            "imageUrl": "https://www.myhome.go.kr/images/portal/myhomeinfo/guideimg/newStay_03.jpg"
          },
          "profile": {
            "imageUrl": "https://www.myhome.go.kr/images/portal/myhomeinfo/guideimg/newStay_03.jpg",
            "nickname": "상세안내"
          },
          "buttons": [
            {
              "action": "webLink",
              "label": info_data.iloc[0]['site'],
              "webLinkUrl": info_data.iloc[0]['address']
            },
            {
              "action": "webLink",
              "label": info_data.iloc[1]['site'],
              "webLinkUrl": info_data.iloc[1]['address']
            },
            {
              "action": "webLink",
              "label": info_data.iloc[2]['site'],
              "webLinkUrl": info_data.iloc[2]['address']
            },
            {
              "action": "webLink",
              "label": info_data.iloc[3]['site'],
              "webLinkUrl": info_data.iloc[3]['address']}]}})
    
    res['template']['outputs'].append({
        "basicCard": {
          "title": "공공지원민간임대주택 상세안내",
          "thumbnail": {
            "imageUrl": ""
          },
          "buttons": [
            {
              "action": "webLink",
              "label": info_data.iloc[3]['site'],
              "webLinkUrl": info_data.iloc[3]['address']}]}})
    
    res['template']['outputs'].append({"basicCard": {"title": welfare_type + " 링크", "description": "자세한 사항은 링크 연결로...",
                            "thumbnail": {"imageUrl": ""},
                            "buttons": [{
                                        "label": "링크연결",
                                        "action": "webLink",
                                        "webLinkUrl": URL + service_code[welfare_type]}]}})
    
    for i in range(len(reply[welfare_type])):
        tmp_list = list(reply[welfare_type][i].items())
        tmp_quickReplies_set['quickReplies'].append({"label": tmp_list[0][0], "action": "block", 
                                                     "blockId": tmp_list[0][1], "extra": {"welfare_type" : welfare_type}})

    
    tmp_quickReplies_set['quickReplies'].append({"label": "주택복지", "action": "block", 
                                                     "blockId": big_reply['주택복지']})
    tmp_quickReplies_set['quickReplies'].append({"label": "메인메뉴", "action": "block", 
                                                     "blockId": big_reply['메인메뉴']})
    
    res['template'].update(tmp_quickReplies_set)
        
    return jsonify(res)