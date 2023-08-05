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


class Instrument(Model):
    """Instrument.

    :param href:
    :type href: str
    :param lusid_instrument_id: The lusid instrument id (LUID) of the
     instrument
    :type lusid_instrument_id: str
    :param version: The version of the instrument
    :type version: ~lusidtr.models.Version
    :param name: The name of the instrument
    :type name: str
    :param identifiers: The set of identifiers that can be used to uniquely
     identify the instrument
    :type identifiers: dict[str, str]
    :param properties: Any requested instrument properties. If no property can
     be found for the instrument, then
     a value of 'Unknown' will be returned
    :type properties: list[~lusidtr.models.Property]
    :param lookthrough_portfolio: The lookthrough portfolio of the instrument
     (if any).
    :type lookthrough_portfolio: ~lusidtr.models.ResourceId
    :param instrument_definition: The economic definition of the instrument
     for an OTC or instrument where an expanded definition exists.
    :type instrument_definition: ~lusidtr.models.InstrumentEconomicDefinition
    :param state: Possible values include: 'Active', 'Inactive'
    :type state: str or ~lusidtr.models.enum
    :param links:
    :type links: list[~lusidtr.models.Link]
    """

    _attribute_map = {
        'href': {'key': 'href', 'type': 'str'},
        'lusid_instrument_id': {'key': 'lusidInstrumentId', 'type': 'str'},
        'version': {'key': 'version', 'type': 'Version'},
        'name': {'key': 'name', 'type': 'str'},
        'identifiers': {'key': 'identifiers', 'type': '{str}'},
        'properties': {'key': 'properties', 'type': '[Property]'},
        'lookthrough_portfolio': {'key': 'lookthroughPortfolio', 'type': 'ResourceId'},
        'instrument_definition': {'key': 'instrumentDefinition', 'type': 'InstrumentEconomicDefinition'},
        'state': {'key': 'state', 'type': 'str'},
        'links': {'key': 'links', 'type': '[Link]'},
    }

    def __init__(self, href=None, lusid_instrument_id=None, version=None, name=None, identifiers=None, properties=None, lookthrough_portfolio=None, instrument_definition=None, state=None, links=None):
        super(Instrument, self).__init__()
        self.href = href
        self.lusid_instrument_id = lusid_instrument_id
        self.version = version
        self.name = name
        self.identifiers = identifiers
        self.properties = properties
        self.lookthrough_portfolio = lookthrough_portfolio
        self.instrument_definition = instrument_definition
        self.state = state
        self.links = links
