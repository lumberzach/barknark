from twilio.rest import Client
from dotenv import load_dotenv
from twilio.twiml.messaging_response import MessagingResponse
import os
from flask import Flask, request, redirect
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

"""
Program that will allow passerbys to text a twilio number commands if my dog is barking from the balcony while I am not home.
If triggered, a Raspberry Pi will initiate misters to spray down from the balcony forcing her back inside.
If she is not barking, they can trigger a treat to be deployed.
"""



# Account SID and Auth Token from Twilio account
load_dotenv()
account_sid = os.getenv('sid')
auth_token = os.getenv('token')

client = Client(account_sid, auth_token)


# Dispenses treat
def treat_dispenser():
    "Dispense Treat Raspberry Pi Placeholder"
    treat_dispenser.counter += 1
    print(treat_dispenser.counter)
    return treat_dispenser.counter


# Sprays mists
def mist_dispenser():
    "Mists of Doom Raspberry Pi Placeholder"
    mist_dispenser.counter += 1
    print(mist_dispenser.counter)
    return mist_dispenser.counter


# Snaps photo from Raspberry Pi Cam
def snap_photo():
    "Snap photo / video Raspberry Pi Placeholder"
    pass


# Updates Google Sheet with the text content and phone number
def update_gsheet(reply, number):
    # Google Spreadsheets auth
    scope = ['https://spreadsheets.google.com/feeds']
    gc = gspread.service_account(filename='client_secret.json')
    sh = gc.open_by_key("1BRsC8OSGkPuSonT28GR1UlizA3lKLS2JDPI6nIX8RJU")  # ID in URL of sheet
    sheet = sh.sheet1
    row = [reply, number]
    index = 1
    sheet.insert_row(row, index)
    print("gsheet updated")


# Setting counters to 0
treat_dispenser.counter = 0
mist_dispenser.counter = 0


# Flask, webpage displaying number and commands
app = Flask(__name__)
@app.route('/')
def display():
    return '(555)-555-5555 | Text WOOF if she is barking, text TREAT if she is being a good girl!'


# Twilio SMS handling and main script
@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # TwiML response
    resp = MessagingResponse()
    body = request.values.get('Body', None)
    number = request.values.get('From', None)

    print(f"Message received from {number}, it said: {body}")

    if body.lower().strip() == "treat" and treat_dispenser.counter < 5:
        print("Good girls get all the treats!")
        treat_dispenser()
        snap_photo()
        resp.message("She will receive a treat now, thanks for helping train this good girl!")
        update_gsheet(body, number)

    elif body.lower().strip() == "treat":
        resp.message("Coco is out of treats for the day due to being such a good girl!")
        update_gsheet(body, number)

    elif body.lower().strip() == "woof" and mist_dispenser.counter < 5:
        print("Good girls get all the treats!")
        mist_dispenser()
        snap_photo()
        resp.message("Thank you for Narking on the Barking. She will endure the mists of doom!")
        update_gsheet(body, number)


    elif body.lower().strip() == "woof":
        print("We are out of water")
        snap_photo()
        resp.message("The mists of doom have run out of water, we will refill soon!")
        update_gsheet(body, number)

    else:
        resp.message("We received your message, but it wasn't one of the valid commands (WOOF or TREAT). We will record it as feedback. Thank you!")
        snap_photo()
        update_gsheet(body, number)

    return str(resp)


app.run()
