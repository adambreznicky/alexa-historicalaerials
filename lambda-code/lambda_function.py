"""
Built from Alexa Skill example, info here: http://amzn.to/1LzFrj6
"""

from __future__ import print_function
import requests
import json
from datetime import datetime
import responses

alexa = responses.alexa()

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
                    "Information System. " + alexa.instruction
    # If the user either does not reply to the welcome message or
    # says something that is not understood, they will be prompted again
    # with this text.
    reprompt_text = alexa.instruction
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


def create_session_ref(county):
    return {"county": county}


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


def get_imagery_years_list(fips):
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
        return unique_years


def confirm_year(years, requested_year):
    multiple = isinstance(years, list)
    year_num = int(requested_year)
    if multiple:
        if year_num in years:
            return True
        else:
            return min(years, key=lambda x: abs(x-year_num))
    elif years == 0:
        return None
    else:
        if year_num == years:
            return True
        else:
            return False


def lookup_session(intent, session):
    """
    Looks up general information on file on a county
    """
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'County' in intent['slots']:
        try:
            historical_county = intent['slots']['County']['value']
            session_attributes = create_session_ref(historical_county)
            fips = get_county_fips(historical_county)
            years = get_hist_imagery_years(fips)
            multiple = isinstance(years, list)

            if multiple:
                reprompt_text = alexa.reprompt_1
                text = alexa.imagery_range(historical_county, years[0],
                                           years[1], years[2])
                speech_output = text + reprompt_text
            elif years == 0:
                reprompt_text = alexa.reprompt_2
                text = alexa.imagery_none(historical_county)
                speech_output = text + reprompt_text
            else:
                reprompt_text = alexa.reprompt_1
                text = alexa.imagery_single(historical_county, years)
                speech_output = text + reprompt_text
        except:
            speech_output = alexa.confused + "Please try again."
            reprompt_text = alexa.confused + alexa.instruction
    else:
        speech_output = alexa.confused + "Please try again."
        reprompt_text = alexa.confused + alexa.instruction
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def list_years_session(intent, session):
    """
    Lists the specific years on file for a county
    """
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if session.get('attributes', {}) and "county" in session.get('attributes',
                                                                 {}):
        session_county = session['attributes']['county']
    else:
        session_county = ""
    print(session_county)
    if 'County' in intent['slots']:
        try:
            historical_county = intent['slots']['County']['value']
            if session_county != historical_county:
                session_attributes = create_session_ref(historical_county)
            fips = get_county_fips(historical_county)
            years = get_imagery_years_list(fips)
            multiple = isinstance(years, list)

            if multiple:
                reprompt_text = alexa.reprompt_1
                text = alexa.list_range(historical_county, years)
                speech_output = text + reprompt_text
            elif years == 0:
                reprompt_text = alexa.reprompt_2
                text = alexa.imagery_none(historical_county)
                speech_output = text + reprompt_text
            else:
                reprompt_text = alexa.reprompt_1
                text = alexa.imagery_single(historical_county, years)
                speech_output = text + reprompt_text
        except:
            try:
                if session_county == "":
                    msg = 'No county saved in session and no new ' \
                          'county requested.'
                    print(msg)
                    raise Exception(msg)
                session_attributes = create_session_ref(session_county)
                fips = get_county_fips(session_county)
                years = get_imagery_years_list(fips)
                multiple = isinstance(years, list)

                if multiple:
                    reprompt_text = alexa.reprompt_1
                    text = alexa.list_range(session_county, years)
                    speech_output = text + reprompt_text
                elif years == 0:
                    reprompt_text = alexa.reprompt_2
                    text = alexa.imagery_none(session_county)
                    speech_output = text + reprompt_text
                else:
                    reprompt_text = alexa.reprompt_1
                    text = alexa.imagery_single(session_county, years)
                    speech_output = text + reprompt_text
            except:
                speech_output = alexa.confused + "Please try again."
                reprompt_text = alexa.confused + alexa.instruction
    else:
        speech_output = alexa.confused + "Please try again."
        reprompt_text = alexa.confused + alexa.instruction
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def specific_year_session(intent, session):
    """
    Verify a specific year on file for a county
    """
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if session.get('attributes', {}) and "county" in session.get('attributes',
                                                                 {}):
        session_county = session['attributes']['county']
    else:
        session_county = ""
    print(session_county)
    if 'County' in intent['slots'] and 'ImageryYear' in intent['slots']:
        try:
            historical_county = intent['slots']['County']['value']
            if session_county != historical_county:
                session_attributes = create_session_ref(historical_county)
            try:
                requested_year = intent['slots']['ImageryYear']['value']
                fips = get_county_fips(historical_county)
                years = get_imagery_years_list(fips)
                multiple = isinstance(years, list)
                confirmation = confirm_year(years, requested_year)

                if multiple:
                    reprompt_text = alexa.reprompt_3
                    if confirmation is True:
                        text = alexa.affirmative_year(historical_county,
                                                      requested_year)
                    else:
                        text = alexa.negative_year(historical_county,
                                                   requested_year,
                                                   confirmation)
                    speech_output = text + reprompt_text
                elif years == 0:
                    reprompt_text = alexa.reprompt_2
                    text = alexa.imagery_none(historical_county)
                    speech_output = text + reprompt_text
                else:
                    reprompt_text = alexa.reprompt_1
                    if confirmation is True:
                        text = alexa.affirmative_year(historical_county,
                                                      requested_year)
                    else:
                        text = alexa.negative_year_single(historical_county,
                                                          requested_year,
                                                          years)
                    speech_output = text + reprompt_text
            except:
                speech_output = alexa.confused_2 + "Please try again."
                reprompt_text = alexa.confused_2 + alexa.instruction

        except:
            try:
                if session_county == "":
                    msg = 'No county saved in session and no new ' \
                          'county requested.'
                    print(msg)
                    raise Exception(msg)
                else:
                    session_attributes = create_session_ref(session_county)

                try:
                    requested_year = intent['slots']['ImageryYear']['value']
                    fips = get_county_fips(session_county)
                    years = get_imagery_years_list(fips)
                    multiple = isinstance(years, list)
                    confirmation = confirm_year(years, requested_year)

                    if multiple:
                        reprompt_text = alexa.reprompt_3
                        if confirmation is True:
                            text = alexa.affirmative_year(session_county,
                                                          requested_year)
                        else:
                            text = alexa.negative_year(session_county,
                                                       requested_year,
                                                       confirmation)
                        speech_output = text + reprompt_text
                    elif years == 0:
                        reprompt_text = alexa.reprompt_2
                        text = alexa.imagery_none(session_county)
                        speech_output = text + reprompt_text
                    else:
                        reprompt_text = alexa.reprompt_1
                        if confirmation is True:
                            text = alexa.affirmative_year(session_county,
                                                          requested_year)
                        else:
                            text = alexa.negative_year_single(session_county,
                                                              requested_year,
                                                              years)
                        speech_output = text + reprompt_text
                except:
                    speech_output = alexa.confused_2 + "Please try again."
                    reprompt_text = alexa.confused_2 + alexa.instruction

            except:
                speech_output = alexa.confused + "Please try again."
                reprompt_text = alexa.confused + alexa.instruction
    else:
        speech_output = alexa.confused + "Please try again."
        reprompt_text = alexa.confused + alexa.instruction
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


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
    if intent_name == "SpecificYearIntent":
        return specific_year_session(intent, session)
    elif intent_name == "ListYearsIntent":
        return list_years_session(intent, session)
    elif intent_name == "LookupIntent":
        return lookup_session(intent, session)
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
    Uncomment this if statement and populate with your skill's application ID
    to prevent someone else from configuring a skill that sends requests to
    this function.
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
