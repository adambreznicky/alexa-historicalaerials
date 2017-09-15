"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import requests
import json
from datetime import datetime

# --------------- Helpers that build all of the responses ---------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# -------------- Functions that control the skill's behavior -----------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Howdy! Welcome to the Texas Natural Resources " \
                    "Information System. Please tell me the Texas county " \
                    "you would like historic imagery for and I can tell you " \
                    "what we have in our archive."
    # If the user either does not reply to the welcome message or
    # says something that is not understood, they will be prompted again
    # with this text.
    reprompt_text = "Please tell me the Texas county you would like " \
                    "historic imagery for."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Goodbye"
    speech_output = "Thanks for chatting with TinRiss. Goodbye."
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


# def create_favorite_color_attributes(favorite_color):
#     return {"favoriteColor": favorite_color}


def get_county_fips(name):
    with open('counties_lower.json') as json_data:
        d = json.load(json_data)
        lower = name.lower()
        fips = d[lower]
        return fips


def format_year_list(the_list):
    no_none = [value for value in the_list if value is not None]
    return [datetime.strptime(i,
            '%Y-%m-%dT%H:%M:%S.%fZ').year for i in no_none]


def get_hist_imagery_years(fips):
    url_base = 'https://historical-aerials.tnris.org/api/v1/' \
               'records?countyFips='
    url = url_base + str(fips)
    r = requests.get(url)
    imgs = r.json()
    if len(imgs) == 0:
        return 0
    if len(imgs) == 1:
        single_year = imgs[0]['Date']
        try:
            year = datetime.strptime(single_year, '%Y-%m-%dT%H:%M:%S.%fZ').year
            return year
        except:
            return 0
    else:
        try:
            years = [datetime.strptime(i['Date'],
                     '%Y-%m-%dT%H:%M:%S.%fZ').year for i in imgs]
        except:
            init = [i['Date'] for i in imgs]
            years = format_year_list(init)

        unique_years = sorted(set(years))
        print(unique_years)
        oldest = unique_years[0]
        newest = unique_years[-1]
        length = len(unique_years)
        return [length, oldest, newest]


def lookup_session(intent, session):
    """
    Looks up requested data
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'County' in intent['slots']:
        try:
            historical_county = intent['slots']['County']['value']
            # session_attributes = create_favorite_color_attributes(favorite_color)
            fips = get_county_fips(historical_county)
            years = get_hist_imagery_years(fips)
            multiple = isinstance(years, list)

            if multiple:
                speech_output = "TinRiss has " + str(years[0]) + " years of " \
                                + historical_county + " County historical " \
                                "imagery available ranging from " + \
                                str(years[1]) + " to " + str(years[2]) + ". " \
                                "Is there another county you would " \
                                "like me to look up?"
                reprompt_text = "Is there another county you would " \
                                "like me to look up?"
            elif years == 0:
                speech_output = "Sorry, there is no historical imagery " + \
                                "for " + historical_county + " County. " \
                                "If there is another county I can lookup " \
                                "I would be happy to do so."
                reprompt_text = "If there is another county I can lookup " \
                                "I would be happy to do so."
            else:
                speech_output = "TinRiss has 1 year of " + \
                                historical_county + " County historical " \
                                "imagery available. It is from " + str(years) \
                                + ". " + \
                                "Is there another county you would " \
                                "like me to look up?"
                reprompt_text = "Is there another county you would " \
                                "like me to look up?"
        except:
            speech_output = "I'm not sure what county you're looking for. " \
                            "Please try again."
            reprompt_text = "I'm not sure what county you're looking for. " \
                            "Please tell me the Texas county you would like " \
                            "historic imagery for."

    else:
        speech_output = "I'm not sure what county you're looking for. " \
                        "Please try again."
        reprompt_text = "I'm not sure what county you're looking for. " \
                        "Please tell me the Texas county you would like " \
                        "historic imagery for."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# def get_color_from_session(intent, session):
#     session_attributes = {}
#     reprompt_text = None

#     if session.get('attributes', {}) and "favoriteColor" in session.get('attributes', {}):
#         favorite_color = session['attributes']['favoriteColor']
#         speech_output = "Your favorite color is " + favorite_color + \
#                         ". Goodbye."
#         should_end_session = True
#     else:
#         speech_output = "I'm not sure what your favorite color is. " \
#                         "You can say, my favorite color is red."
#         should_end_session = False

#     # Setting reprompt_text to None signifies that we do not want to reprompt
#     # the user. If the user does not respond or says something that is not
#     # understood, the session will end.
#     return build_response(session_attributes, build_speechlet_response(
#         intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" +
          session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    print(intent_name)

    # Dispatch to your skill's intent handlers
    if intent_name == "LookupIntent":
        return lookup_session(intent, session)
    # elif intent_name == "WhatsMyColorIntent":
    #     return get_color_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif (intent_name == "AMAZON.CancelIntent" or
          intent_name == "AMAZON.StopIntent"):
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
