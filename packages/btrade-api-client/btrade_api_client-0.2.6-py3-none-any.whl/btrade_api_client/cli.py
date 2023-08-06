"""
Command line client for the Bit Trade API
"""
import argparse
import json
import logging

from btrade_api_client.client import ApiClient
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

logging.basicConfig(level=logging.INFO)

"""
Pretty print a JSON object
"""
def pretty_print(json_object):
    json_str = json.dumps(json_object, indent=4, sort_keys=True)
    print(highlight(json_str, JsonLexer(), TerminalFormatter()))

def run_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('operation',
                        choices=['quote', 'wallets', 'bankaccounts', 'balance',
                                 'orders', 'order', 'transactions', 'ticker'])
    parser.add_argument('--key', help='btrade.io API key', required=True)
    parser.add_argument('--secret', help='btrade.io API secret', required=True)
    parser.add_argument('--src')
    parser.add_argument('--dst')
    parser.add_argument('--src-volume')
    parser.add_argument('--dst-volume')
    parser.add_argument('--price')
    parser.add_argument('--currency')
    parser.add_argument('--endpoint', default="https://api.dev.btrade.io")
    parser.add_argument('--accept', default=0)
    parser.add_argument('--wallet-id')
    parser.add_argument('--wallet-address')
    parser.add_argument('--bankaccount')
    parser.add_argument('--order')
    parser.add_argument('--ticker')

    args = parser.parse_args()
    c = ApiClient(args.key, args.secret, args.endpoint)

    if args.operation == 'wallets':
        pretty_print(c.wallets())
    elif args.operation == 'ticker':
        pretty_print(c.ticker())
    elif args.operation == 'orders':
        pretty_print(c.orders())
    elif args.operation == 'order':
        pretty_print(c.order(args.order))
    elif args.operation == 'bankaccounts':
        pretty_print(c.bank_accounts())
    elif args.operation == 'balance':
        pretty_print(c.balance(args.currency))
    elif args.operation == 'transactions':
        pretty_print(c.transactions(args.currency))
    elif args.operation == 'quote':
        quote = c.quote(args.src, args.dst, args.src_volume, args.dst_volume)
        pretty_print(quote)
        if quote and args.accept:
            res = c.accept(quote['token'], args.wallet_id, args.wallet_address, args.bankaccount)
            if res:
                pretty_print(res)

if __name__ == "__main__":
    run_cli()