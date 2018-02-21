# [START import_libraries]
import argparse
import uuid

import dialogflow
# [END import_libraries]
project_id = "fmla-faq"
language_code = "en-US"
#session_id = str(uuid.uuid4())
session_id = "testSession"
text = "thisisanothertestforeric"

# [START dialogflow_detect_intent_text]
def detect_intent_texts():
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    client_context = dialogflow.ContextsClient()
#    context = client_context.get_context("projects/fmla-faq/agent/sessions/b805e39f-3d28-4222-b159-cb46776ef1dc/contexts/randomtestforeric-followup")
#    dialogflow.types.Context(name="projects/fmla-faq/agent/sessions/e8704b67-400f-4a90-bdfb-6b58db4bf3b4/contexts/randomtestforeric-followup", lifespan_count=1, parameters = "{fields {key: \"date\" value {string_value: ""}}fields {key: \"date.original\" value {string_value: \"\"}} fields { key: \"geo-city\" value { string_value: \"\" } } fields { key: \"geo-city.original\" value { string_value: \"\" } } fields { key: \"geo-state\" value { string_value: \"\" } } fields { key: \"geo-state.original\" value { string_value: \"\" } } } ")

#    query_params = dialogflow.types.QueryParameters(contexts=context)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
        response.query_result.fulfillment_text))
    print('Parameter text: {}\n'.format(
        response.query_result.parameters))
    print('Output context: {}\n'.format(
        response.query_result.output_contexts))
    print("***********************************")
#    print(response.query_result.output_contexts.pop())
    print(response.query_result.output_contexts)


#    context = client_context.get_context(response.query_result.output_contexts.parameters)
#    print(context.lifespan_count)


detect_intent_texts()
