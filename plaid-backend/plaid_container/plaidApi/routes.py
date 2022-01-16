
from flask import Flask, request, jsonify, url_for, Blueprint
from . import bp
from plaid.model.products import Products
import os
import json 
import requests
import plaid 
from .plaidFunctions import info, create_link_token_for_payment, create_link_token, get_accounts
from plaid.api import plaid_api
# https://plaid.github.io/plaid-python/contents.html
# three different Plaid environments.
# plaid_python==8.8.0

# Fill in your Plaid API keys - https://dashboard.plaid.com/account/keys
PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')


PLAID_ENV = os.getenv('PLAID_ENV', 'sandbox')
#  'assets' in order for the app to be able to create and retrieve asset reports.
PLAID_PRODUCTS = os.getenv('PLAID_PRODUCTS', 'transactions').split(',')
PLAID_COUNTRY_CODES = os.getenv('PLAID_COUNTRY_CODES', 'US').split(',')


def empty_to_none(field):
    value = os.getenv(field)
    if value is None or len(value) == 0:
        return None
    return value

host = plaid.Environment.Sandbox

if PLAID_ENV == 'sandbox':
    host = plaid.Environment.Sandbox

if PLAID_ENV == 'development':
    host = plaid.Environment.Development

if PLAID_ENV == 'production':
    host = plaid.Environment.Production

# Parameters used for the OAuth redirect Link flow.
# Set PLAID_REDIRECT_URI to 'http://localhost:3000/'
# The OAuth redirect flow requires an endpoint on the developer's website
# that the bank website should redirect to. You will need to configure
# this redirect URI for your client ID through the Plaid developer dashboard
# at https://dashboard.plaid.com/team/api.
PLAID_REDIRECT_URI = empty_to_none('PLAID_REDIRECT_URI')

configuration = plaid.Configuration(
    host=host,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
        'plaidVersion': '2020-09-14'
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

products = []
for product in PLAID_PRODUCTS:
    products.append(Products(product))


# We store the access_token in memory - in production, store it in a secure
# persistent data store.
access_token = None
# The payment_id is only relevant for the UK Payment Initiation product.
# We store the payment_id in memory - in production, store it in a secure
# persistent data store.
payment_id = None
# The transfer_id is only relevant for Transfer ACH product.
# We store the transfer_id in memomory - in produciton, store it in a secure
# persistent data store
transfer_id = None

item_id = None


@bp.route('/', methods=['POST', 'GET'])
def plaidCall():
    return 'pass'

@bp.route('/api/info', methods=['POST'])
def infoCall():
    info(PLAID_PRODUCTS)
    return 'pass'

@bp.route('/api/create_link_token_for_payment', methods=['POST'])
def create_link_token_for_paymentCall(client):
    create_link_token_for_payment(client)
    return 'pass'

@bp.route('/api/create_link_token', methods=['POST'])
def create_link_tokenCall():
    create_link_token()
    return 'pass'

@bp.route('/api/create_link_token', methods=['POST'])
def create_link_token_OpenVessel_Call():
    create_link_token(client, products, PLAID_COUNTRY_CODES)
    return 'pass'



@bp.route('/api/set_access_token', methods=['POST'])
def get_access_tokenCall():
    get_access_token()
    return 'pass'

@bp.route('/api/auth', methods=['GET'])
def get_authCall():
    get_auth()
    return 'pass'

@bp.route('/api/transactions', methods=['GET'])
def get_transactionsCall():
    get_transactions()
    return 'pass'

@bp.route('/api/identity', methods=['GET'])
def get_identityCall():
    get_identity()
    return 'pass'

@bp.route('/api/balance', methods=['GET'])
def get_balanceCall():
    get_balance()
    return 'pass'

@bp.route('/api/accounts', methods=['GET'])
def get_accountsCall():
    get_accounts()
    return 'pass'

@bp.route('/api/assets', methods=['GET'])
def get_assetsCall():
    get_assets()
    return 'pass'

@bp.route('/api/holdings', methods=['GET'])
def get_holdingsCall():
    get_holdings()
    return 'pass'


@bp.route('/api/investment_transactions', methods=['GET'])
def get_investment_transactionsCall():
    get_investment_transactions()
    return 'pass'


@bp.route('/api/transfer', methods=['GET'])
def transferCall():
    transfer()
    return 'pass'

@bp.route('/api/payment', methods=['GET'])
def paymentCall():
    payment(client)
    return 'pass'

@bp.route('/api/item', methods=['GET'])
def itemCall():
    item()
    return 'pass'