__author__ = 'bliss'

# just for web application. web application need server to help receive the verify sms
# for mobile, it  doesn't need the server to receive sms.

from herovii.api.base import ApiBlueprint

api = ApiBlueprint('sms')

# def send_sms('')