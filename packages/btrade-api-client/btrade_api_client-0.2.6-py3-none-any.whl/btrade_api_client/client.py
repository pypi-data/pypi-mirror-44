#!/usr/bin/env python3
import json
import logging
import requests

from btrade_api_client.auth import Auth


class ApiClient:
    headers = {'content-type': bytes('application/json', 'utf8')}

    def __init__(self, api_key, api_secret, endpoint="https://api.btrade.io"):
        self.endpoint = endpoint
        self.auth = Auth(api_key, api_secret)

    def bank_accounts(self):
        resp = requests.get(self.endpoint + "/bankaccount", auth=self.auth)
        if resp.status_code == 200:
            return resp.json()
        logging.warning("Received HTTP %s with body %s", resp.status_code, resp.text)
        return None

    def wallets(self):
        resp = requests.get(self.endpoint + "/wallet", auth=self.auth)
        if resp.status_code == 200:
            return resp.json()
        logging.warning("Received HTTP %s with body %s", resp.status_code, resp.text)
        return None

    def orders(self):
        resp = requests.get(self.endpoint + "/order", auth=self.auth)
        if resp.status_code == 200:
            return resp.json()
        logging.warning("Received HTTP %s with body %s", resp.status_code, resp.text)
        return None

    def order(self, order_id):
        resp = requests.get(self.endpoint + "/order/" + order_id, auth=self.auth)
        if resp.status_code == 200:
            return resp.json()
        logging.warning("Received HTTP %s with body %s", resp.status_code, resp.text)
        return None

    def quote(self, src, dst, src_volume=None, dst_volume=None):
        if not src:
            logging.warning("Cannot get quote without src_currency")
            return None
        if not dst:
            logging.warning("Cannot get quote without dst_currency")
            return None
        if not src_volume and not dst_volume:
            logging.warning("Cannot get quote without src or dst volume")
            return None
        body = {'src_currency': src,
                'dst_currency': dst,
                'src_volume': src_volume,
                'dst_volume': dst_volume
                }
        resp = requests.post(self.endpoint + "/quote",
                             headers=self.headers, data=json.dumps(body), auth=self.auth)
        if resp.status_code == 200:
            return resp.json()
        logging.warning("Received HTTP %s with body %s", resp.status_code, resp.text)
        return None

    def accept(self, token, wallet_id, wallet_address, bank_account):
        body = {'token': token,
                'wallet_id': wallet_id,
                'wallet_address': wallet_address,
                'bank_account': bank_account}
        resp = requests.post(self.endpoint + "/quote/accept",
                             headers=self.headers, data=json.dumps(body), auth=self.auth)
        if resp.status_code == 200:
            return resp.json()
        logging.warning("Received HTTP %s with body %s", resp.status_code, resp.text)
        return None

    def transactions(self, currency):
        resp = requests.get(self.endpoint + "/transactions/" + currency, auth=self.auth)
        if resp.status_code == 200:
            return resp.json()
        logging.warning("Received HTTP %s with body %s", resp.status_code, resp.text)
        return None

    def balance(self, currency):
        if not currency:
            logging.warning("Currency cannot be None when requesting balance")
            return {}
        resp = requests.get(self.endpoint + "/balance/"+ currency, auth=self.auth)
        if resp.status_code == 200:
            return resp.json()
        logging.warning("Received HTTP %s with body %s", resp.status_code, resp.text)
        return None

    def ticker(self):
        resp = requests.get(self.endpoint + "/ticker")
        if resp.status_code == 200:
            return resp.json()
        logging.warning("Received HTTP %s with body %s", resp.status_code, resp.text)
        return None
