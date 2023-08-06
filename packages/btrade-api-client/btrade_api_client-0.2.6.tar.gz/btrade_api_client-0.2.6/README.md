btrade_api_client
================

Bit Trade API Client library

This document describes the available API calls, for more information on the API vist the [API Documentation](https://btrade.io/api).

Installation
------------

pip3 install btrade-api-client


Usage
================

Create client instance

```python
from btrade_api_client.client import ApiClient
client = ApiClient(api_key, api_secret)
```

Bankaccount
------------
Get customer registered bank accounts

```python
bankaccounts  = client.bankaccounts()
```

See [API Documentation](http://api-docs-btrade.io.s3-website-ap-southeast-2.amazonaws.com/apibank_accounts_list) for response.

Get Wallets
------------
Get customer registered wallets

```python
wallets  = client.wallets()
```

See [API Documentation](http://api-docs-btrade.io.s3-website-ap-southeast-2.amazonaws.com/#apiwallets_list) for response.


Get Orders
------------
Get all orders

```python
orders  = client.orders()
```

See [API Documentation](http://api-docs-btrade.io.s3-website-ap-southeast-2.amazonaws.com/#apiorders) for response.


Get Order
------------
Get single order details

```python
order  = client.order(12345)
```

See [API Documentation](http://api-docs-btrade.io.s3-website-ap-southeast-2.amazonaws.com/#apiorder_by_id) for response.


Get Quote
------------

To get a quote from the API use the quote method as below.

```python
quote  = client.quote(src="aud", dst="btc", dst_volume=1, src_volume=None)
```

See [API Documentation](http://api-docs-btrade.io.s3-website-ap-southeast-2.amazonaws.com/#apiquote) for response.


Accept Quote
------------

To accept a quote use the `token` from the quote, and one of the following scenarios :

To an existing wallet :
```python
order = c.accept(quote['token'], wallet_id=12345)
```

To a new wallet with the given address :
```python
order = c.accept(quote['token'], wallet_address=3abcdf12345)
```

To an existing bank account, this is only valid when the dst currency is a fiat currency:
```python
order = c.accept(quote['token'], bank_account=12345)
```

See [API Documentation](http://api-docs-btrade.io.s3-website-ap-southeast-2.amazonaws.com/#apiquote_accept) for response.


Get Transactions
------------

Get all customer transactions for the given currency

```python
transactions  = client.transactions("aud")
```

See [API Documentation](http://api-docs-btrade.io.s3-website-ap-southeast-2.amazonaws.com/#apitransactions) for response.


Get Balance
------------

Get current balance for the given currency

```python
balance  = client.balance("aud")
```

See [API Documentation](http://api-docs-btrade.io.s3-website-ap-southeast-2.amazonaws.com/#apibalance) for response.


Get Ticker
------------

Get current indicative rates

```python
tickers  = client.ticker()
```

See [API Documentation](http://api-docs-btrade.io.s3-website-ap-southeast-2.amazonaws.com/#apiticker) for response.


Credits
------------

This library is based on https://github.com/guardian/httpie-hmac-auth/