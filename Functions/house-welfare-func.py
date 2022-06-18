from flask import Blueprint

a_api = Blueprint('a_api', __name__)

@a_api.route('/housing_welfare/total-public-des', methods=['POST'])
def total_public_des(): 
"""    body = request.get_json()
    print(body)
    print(body['userRequest']['utterance'])"""

    responseBody = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "안녕 hello I'm Ryan"
                    }
                }
            ]
        }
    }

    return responseBody