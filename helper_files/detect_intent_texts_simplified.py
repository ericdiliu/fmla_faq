# [START import_libraries]
import argparse
import uuid

import dialogflow
# [END import_libraries]
project_id = "fmla-faq"
language_code = "en-US"
session_id = str(uuid.uuid4())
text = "What is FMLA?"

# [START dialogflow_detect_intent_text]
def detect_intent_texts():
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
        response.query_result.fulfillment_text))


detect_intent_texts()
