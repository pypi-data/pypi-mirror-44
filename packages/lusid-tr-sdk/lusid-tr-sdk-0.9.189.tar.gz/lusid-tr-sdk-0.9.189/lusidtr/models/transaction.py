# coding=utf-8
# --------------------------------------------------------------------------
# # License
#
# Copyright &copy; 2018 FINBOURNE TECHNOLOGY LTD
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class Transaction(Model):
    """Transaction.

    :param transaction_id:
    :type transaction_id: str
    :param type:
    :type type: str
    :param instrument_identifiers:
    :type instrument_identifiers: dict[str, str]
    :param instrument_uid:
    :type instrument_uid: str
    :param transaction_date:
    :type transaction_date: datetime
    :param settlement_date:
    :type settlement_date: datetime
    :param units:
    :type units: float
    :param transaction_price:
    :type transaction_price: ~lusidtr.models.TransactionPrice
    :param total_consideration:
    :type total_consideration: ~lusidtr.models.CurrencyAndAmount
    :param exchange_rate:
    :type exchange_rate: float
    :param transaction_currency: This is the ISO three letter code
     representing the transaction currency
    :type transaction_currency: str
    :param properties:
    :type properties: list[~lusidtr.models.PerpetualProperty]
    :param counterparty_id:
    :type counterparty_id: str
    :param source:
    :type source: str
    :param netting_set:
    :type netting_set: str
    """

    _validation = {
        'transaction_id': {'required': True},
        'type': {'required': True},
        'instrument_uid': {'required': True},
        'transaction_date': {'required': True},
        'settlement_date': {'required': True},
        'units': {'required': True},
        'transaction_price': {'required': True},
        'total_consideration': {'required': True},
        'source': {'required': True},
    }

    _attribute_map = {
        'transaction_id': {'key': 'transactionId', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
        'instrument_identifiers': {'key': 'instrumentIdentifiers', 'type': '{str}'},
        'instrument_uid': {'key': 'instrumentUid', 'type': 'str'},
        'transaction_date': {'key': 'transactionDate', 'type': 'iso-8601'},
        'settlement_date': {'key': 'settlementDate', 'type': 'iso-8601'},
        'units': {'key': 'units', 'type': 'float'},
        'transaction_price': {'key': 'transactionPrice', 'type': 'TransactionPrice'},
        'total_consideration': {'key': 'totalConsideration', 'type': 'CurrencyAndAmount'},
        'exchange_rate': {'key': 'exchangeRate', 'type': 'float'},
        'transaction_currency': {'key': 'transactionCurrency', 'type': 'str'},
        'properties': {'key': 'properties', 'type': '[PerpetualProperty]'},
        'counterparty_id': {'key': 'counterpartyId', 'type': 'str'},
        'source': {'key': 'source', 'type': 'str'},
        'netting_set': {'key': 'nettingSet', 'type': 'str'},
    }

    def __init__(self, transaction_id, type, instrument_uid, transaction_date, settlement_date, units, transaction_price, total_consideration, source, instrument_identifiers=None, exchange_rate=None, transaction_currency=None, properties=None, counterparty_id=None, netting_set=None):
        super(Transaction, self).__init__()
        self.transaction_id = transaction_id
        self.type = type
        self.instrument_identifiers = instrument_identifiers
        self.instrument_uid = instrument_uid
        self.transaction_date = transaction_date
        self.settlement_date = settlement_date
        self.units = units
        self.transaction_price = transaction_price
        self.total_consideration = total_consideration
        self.exchange_rate = exchange_rate
        self.transaction_currency = transaction_currency
        self.properties = properties
        self.counterparty_id = counterparty_id
        self.source = source
        self.netting_set = netting_set
