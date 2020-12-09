
from twilio.rest import Client


account_sid = 'AC6f5918413acb9a799db15a6acaf971e6'
auth_token = '9e0cba0dd97d3feae83f5ea0bc4f4841'
client = Client(account_sid, auth_token)

def verifications(phone_number):
        return client.verify \
                    .services('VA82404d36fa7d8d588af6d0231518a8b0') \
                    .verifications \
                    .create(to=phone_number, channel='sms')

def verification_checks(phone_number,token):
        return client.verify \
                    .services('VA82404d36fa7d8d588af6d0231518a8b0') \
                    .verification_checks \
                    .create(to=phone_number, code=token)
                    