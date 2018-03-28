from chatbot_simplebot import simplebot
import os
# import requests
import json
# import argparse
# import uuid
import dialogflow
from hashlib import sha256

from chatbot_simplebot.simplebot import SimpleHandler
from helper_files.dialogflow_parameters import para_to_dict


class FmlaHandler(SimpleHandler):

    @staticmethod
    def getEnvironment(param):
        # param.update({'path_root': os.path.dirname(os.path.abspath(__file__))})
        env = simplebot.SimpleHandler.getEnvironment(param)
        return env

    def process_post(self, resultObj):
        """
        Customized processing function for producing a result.
        """

        # Settings for google project
        project_id = "fmla-faq"
        language_code = "en-US"
        session_id = sha256(str.encode(resultObj['from'])).hexdigest()

        text = resultObj['message']
        session_client = dialogflow.SessionsClient()

        session = session_client.session_path(project_id, session_id)
        print('Session path: {}\n'.format(session))

        text_input = dialogflow.types.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        # Find information from fmla_faq.json
        fmla_faq_dict = json.loads(open('fmla_faq.json', 'r').read())
        fmla_status_dict = json.loads(open('fmla_status.json', 'r').read())

        print('=' * 20)  # separator
        print('Query text: {}'.format(response.query_result.query_text))  # query user sent

        # Detected intent and confidence from Dialogflow
        print('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))

        # Fulfilment text, parameter, and context from Dialogflow
        print('Fulfillment text: {}\n'.format(
            response.query_result.fulfillment_text))
        print('Parameter text: {}\n'.format(
            response.query_result.parameters))
        print('Output context: {}\n'.format(
            response.query_result.output_contexts))

        detected_intent = response.query_result.intent.display_name

        if detected_intent == 'fmla-status':
            # find fmla status from fmla_status.json
            # to be replaced with actual data from LeaveLink
            leave_number = int(para_to_dict(response.query_result.parameters).get('leavenumber'))
            if leave_number != '':
                if leave_number % 5 == 1:
                    resultObj['result'] = fmla_status_dict.get('status1')
                elif leave_number % 5 == 2:
                    resultObj['result'] = fmla_status_dict.get('status2')
                elif leave_number % 5 == 3:
                    resultObj['result'] = fmla_status_dict.get('status3')
                elif leave_number % 5 == 4:
                    resultObj['result'] = fmla_status_dict.get('status4')
                else:
                    resultObj['result'] = fmla_status_dict.get('status5')
            else:
                resultObj['result'] = response.query_result.fulfillment_text
        elif detected_intent in fmla_faq_dict:
            # find FAQ answer from fmla_faq.json
            resultObj['result'] = fmla_faq_dict.get(detected_intent)
        else:
            resultObj['result'] = response.query_result.fulfillment_text
        print(resultObj['result'])
        print(resultObj)

        return resultObj


if __name__ == "__main__":
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))     # add path
    defArgs = {'port': 8899, 'verbose': True}        # default args
    if len(sys.argv) > 2:                                             # add user/password
        defArgs['bot_name'] = sys.argv[1]
        defArgs['bot_secret'] = sys.argv[2]
        defArgs['json_response'] = True

    print("Launching console-interactive server... [credentials? run {:} <bot_user> <pass> ]".format(sys.argv[0]))
    print()
    FmlaHandler.serve_forever(defArgs, FmlaHandler)
