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


class ReferencePortfolioConstituentRequest(Model):
    """ReferencePortfolioConstituentRequest.

    :param instrument_identifiers:
    :type instrument_identifiers: dict[str, str]
    :param properties:
    :type properties: dict[str, ~lusidtr.models.PerpetualPropertyValue]
    :param weight:
    :type weight: float
    :param currency:
    :type currency: str
    """

    _validation = {
        'instrument_identifiers': {'required': True},
        'weight': {'required': True},
    }

    _attribute_map = {
        'instrument_identifiers': {'key': 'instrumentIdentifiers', 'type': '{str}'},
        'properties': {'key': 'properties', 'type': '{PerpetualPropertyValue}'},
        'weight': {'key': 'weight', 'type': 'float'},
        'currency': {'key': 'currency', 'type': 'str'},
    }

    def __init__(self, instrument_identifiers, weight, properties=None, currency=None):
        super(ReferencePortfolioConstituentRequest, self).__init__()
        self.instrument_identifiers = instrument_identifiers
        self.properties = properties
        self.weight = weight
        self.currency = currency
