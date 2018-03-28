from chatbot_simplebot import simplebot
import os
import requests
import json
import argparse
import uuid
from hashlib import sha256

from chatbot_simplebot.simplebot import SimpleHandler

class FmlaHandler(simplebot.SimpleHandler):

    @staticmethod
    def getEnvironment(param):
        # param.update({'path_root': os.path.dirname(os.path.abspath(__file__))})
        env = simplebot.SimpleHandler.getEnvironment(param)
        return env

    def process_post(self, resultObj):
        """
        Customized processing function for producing a result.
        """

        luis_headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'ba47b37427204e8db8f2a74ab091b628',
        }
        luis_params ={
            # Query parameter
            'q': resultObj['message'],
            # Optional request parameters, set to default values
            'timezoneOffset': '0',
            'verbose': 'false',
            'spellCheck': 'false',
            'staging': 'false',
        }


        luis_r = requests.get('https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/187107d1-442c-4fe8-9734-33a391227af5',headers=luis_headers, params=luis_params)
        print(luis_r.json())
        luis_intent = luis_r.json()['topScoringIntent']['intent']
        luis_intent_confidence = luis_r.json()['topScoringIntent']['score']

        fmla_faq = open('fmla_faq.json', 'r').read()
        fmla_faq_dict = json.loads(fmla_faq)

        print('=' * 20)


        if luis_intent == "testHTML":
            resultObj['result'] = "<table><tr><td>c1r1</td><td>c1r2</td></tr><tr><td>c2r1</td><td>c2r2</td></tr></table><img src='https://1.bp.blogspot.com/-YmpTbsT6ZVo/WLmowwnyc8I/AAAAAAAAAAM/uWyQ7W8XtzMREwhiuqiP-UPKQHQP3TJpwCLcB/s320/iPhone7-jetblack.png'></img><z-button message=\"What is FMLA?\">What is FMLA?</z-button>"
        elif luis_intent in fmla_faq_dict:
            ### find answer from json_data
            resultObj['result'] = fmla_faq_dict.get(luis_intent)
        else:
            resultObj['result'] = "Detected intent is: " + luis_intent + ". Confidence: " + str(luis_intent_confidence)
        print(resultObj['result'])
        print(resultObj)
        ###
#        resultObj['result'] = response.query_result.fulfillment_text
        return resultObj


if __name__ == "__main__":
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))     # add path
    defArgs = {'port':8989, 'verbose':True}        # default args
    if len(sys.argv)>2:                                             # add user/password
        defArgs['bot_name'] = sys.argv[1]
        defArgs['bot_secret'] = sys.argv[2]
        defArgs['json_response']= True

    print("Launching console-interactive server... [credentials? run {:} <bot_user> <pass> ]".format(sys.argv[0]))
    print()
    FmlaHandler.serve_forever(defArgs, FmlaHandler)
