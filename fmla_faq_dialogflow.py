###
# export GOOGLE_APPLICATION_CREDENTIALS="/Users/Liu/Documents/Python/fmla-faq-81f41533d01e.json"
# export GOOGLE_APPLICATION_CREDENTIALS="/Users/ediliu/Documents/PythonProjs/fmla-faq-81f41533d01e.json"
###
from chatbot_simplebot import simplebot
import os
import requests
import json
import argparse
import uuid
import dialogflow

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
        project_id = "fmla-faq"
        language_code = "en-US"
        session_id = str(uuid.uuid4())
        text = resultObj['message']

        session_client = dialogflow.SessionsClient()

        session = session_client.session_path(project_id, session_id)
        print('Session path: {}\n'.format(session))

        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        fmla_faq = open('fmla_faq.json', 'r').read()
        fmla_faq_dict = json.loads(fmla_faq)

        print('=' * 20)
        print('Query text: {}'.format(response.query_result.query_text))
        print('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        print('Fulfillment text: {}\n'.format(
            response.query_result.fulfillment_text))
        ###
        print('Parameter text: {}\n'.format(
            response.query_result.parameters))
        print('Output context: {}\n'.format(
            response.query_result.output_contexts))

        fmla_intent = response.query_result.intent.display_name


        if response.query_result.intent.display_name == "testHTML":
            resultObj['result'] = "<table><tr><td>c1r1</td><td>c1r2</td></tr><tr><td>c2r1</td><td>c2r2</td></tr></table><img src='https://1.bp.blogspot.com/-YmpTbsT6ZVo/WLmowwnyc8I/AAAAAAAAAAM/uWyQ7W8XtzMREwhiuqiP-UPKQHQP3TJpwCLcB/s320/iPhone7-jetblack.png'></img><z-button message=\"What is FMLA?\">What is FMLA?</z-button>"
        elif fmla_intent in fmla_faq_dict:
            ### find answer from json_data
            resultObj['result'] = fmla_faq_dict.get(fmla_intent)
        else:
            resultObj['result'] = response.query_result.fulfillment_text
        print(resultObj['result'])
        print(resultObj)
        ###
#        resultObj['result'] = response.query_result.fulfillment_text
        return resultObj


if __name__ == "__main__":
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))     # add path
    defArgs = {'port':8899, 'verbose':True}        # default args
    if len(sys.argv)>2:                                             # add user/password
        defArgs['bot_name'] = sys.argv[1]
        defArgs['bot_secret'] = sys.argv[2]
        defArgs['json_response']= True

    print("Launching console-interactive server... [credentials? run {:} <bot_user> <pass> ]".format(sys.argv[0]))
    print()
    FmlaHandler.serve_forever(defArgs, FmlaHandler)
