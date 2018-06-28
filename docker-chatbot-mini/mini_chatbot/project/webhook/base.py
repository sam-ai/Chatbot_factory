import os
import requests
from sys import argv
import sys
from random import shuffle
from wit import Wit
from flask import Flask, request, Blueprint
import logging

# Wit.ai parameters
WIT_TOKEN = "K2A2CQCNKELOKHWIVOCFWJSDEH2KIHVT"
# Messenger API parameters
FB_PAGE_TOKEN = "EAAGqvw8s9JcBANS6VyBetvY4ZChfmYWC2wSXG34mZCDUkDW0eBEe4YRZC3MTHTGIiOu2JJldYKCRRjGIcqgK6HVl7DPoupuZC8bPc80HZBc1ERo2L85pvG1QisuhRjHpwzmZBGv0njvQsb4NbIOrXsjwrZCioFpEgXJwNPWwzc9DgZDZD"
# A user secret to verify webhook get request.
FB_VERIFY_TOKEN = "fifa2018"


logging.basicConfig(format='%(message)s')
base_blueprint = Blueprint('base', __name__)



all_jokes = {
    'chuck': [
        'Chuck Norris counted to infinity - twice.',
        'Death once had a near-Chuck Norris experience.',
    ],
    'tech': [
        'Did you hear about the two antennas that got married? The ceremony was long and boring, but the reception was great!',
        'Why do geeks mistake Halloween and Christmas? Because Oct 31 === Dec 25.',
    ],
    'default': [
        'Why was the Math book sad? Because it had so many problems.',
    ],
}


def select_joke(categorey):
    """
    get joke for specific category

    :param categorey: string
    :return: joke
    """
    jokes = all_jokes(categorey or 'deafault')
    shuffle(jokes)

    return jokes[0]




@base_blueprint.route('/webhook', methods=['GET'])
def messenger_webhook():
    """
    A webhook to return a challenge
    """
    verify_token = request.args.get('hub.verify_token')
    # check whether the verify tokens match
    if verify_token == FB_VERIFY_TOKEN:
        # respond with the challenge to confirm
        challenge = request.args.get('hub.challenge')
        return challenge
    else:
        return 'Invalid Request or Verification Token'


# Facebook Messenger POST Webhook
@base_blueprint.route('/webhook', methods=['POST'])
def messenger_post():

    """
    Handler for webhook (currently for postback and messages)
    """
    data = request.json
    # print(data)
    logging.warn("------MESSENGER POST DATA-------")
    logging.warn(data)
    logging.warn("------MESSENGER POST DATA-------")
    if data['object'] == 'page':
        for entry in data['entry']:

            # get all the messages
            messages = entry['messaging']
            if messages[0]:
                # Get the first message
                message = messages[0]
                # Yay! We got a new message!
                # We retrieve the Facebook user ID of the sender
                fb_id = message['sender']['id']
                # We retrieve the message content
                text = message['message']['text']
                # Let's forward the message to Wit /message
                # and customize our response to the message in handle_message
                response = client.message(msg=text, context={'session_id' : fb_id})
                # print(response)
                logging.warn("-------WIT RESPONSE-------")
                logging.warn(response)
                logging.warn("-------WIT RESPONSE-------")
                handle_message(response=response, fb_id=fb_id)
    else:
        # Returned another event
        return 'Received Different Event'

    return "ok", 200


def fb_message(sender_id, text):
    """
    Function for returning response to messenger
    """
    data = {
        'recipient': {'id': sender_id},
        'message': {'text': text}
    }
    # Setup the query string with your PAGE TOKEN
    qs = 'access_token=' + FB_PAGE_TOKEN
    # Send POST request to messenger
    resp = requests.post('https://graph.facebook.com/me/messages?' + qs,
                         json=data)
    return resp.content


def first_entity_value(entities, entity):
    """
    Returns first entity value
    """
    if "intent" not in entities:
        return None
    val = entities["intent"][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val


def handle_message(response, fb_id):

    """
    Customizes our response to the message and sends it
    """
    entities = response['entities']
    # Checks if user's message is a greeting
    # Otherwise we will just repeat what they sent us
    greetings = first_entity_value(entities, 'getstart')
    print(greetings)
    if greetings:
        text = "hello!"
    else:
        text = "We've received your message: " + response['_text']
    # send message
    fb_message(fb_id, text)


# Setup Wit Client
client = Wit(access_token=WIT_TOKEN)