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


class GetReferencePortfolioConstituentsResponse(Model):
    """GetReferencePortfolioConstituentsResponse.

    :param effective_from: The first date from which the weights will apply
    :type effective_from: datetime
    :param weight_type: Indicates the weight reset methods. Static, floating
     or periodical. Possible values include: 'Static', 'Floating', 'Periodical'
    :type weight_type: str or ~lusidtr.models.enum
    :param period_type: Indicates the period type (daily, weekly) that weights
     will reset. Possible values include: 'Daily', 'Weekly', 'Monthly',
     'Quarterly', 'Annually'
    :type period_type: str or ~lusidtr.models.enum
    :param period_count: How many multiples of the period between resets
    :type period_count: int
    :param constituents: Set of constituents (instrument/weight pairings)
    :type constituents: list[~lusidtr.models.ReferencePortfolioConstituent]
    :param href: The Uri that returns the same result as the original request,
     but may include resolved as at time(s).
    :type href: str
    :param links:
    :type links: list[~lusidtr.models.Link]
    """

    _validation = {
        'effective_from': {'required': True},
        'weight_type': {'required': True},
        'constituents': {'required': True},
    }

    _attribute_map = {
        'effective_from': {'key': 'effectiveFrom', 'type': 'iso-8601'},
        'weight_type': {'key': 'weightType', 'type': 'str'},
        'period_type': {'key': 'periodType', 'type': 'str'},
        'period_count': {'key': 'periodCount', 'type': 'int'},
        'constituents': {'key': 'constituents', 'type': '[ReferencePortfolioConstituent]'},
        'href': {'key': 'href', 'type': 'str'},
        'links': {'key': 'links', 'type': '[Link]'},
    }

    def __init__(self, effective_from, weight_type, constituents, period_type=None, period_count=None, href=None, links=None):
        super(GetReferencePortfolioConstituentsResponse, self).__init__()
        self.effective_from = effective_from
        self.weight_type = weight_type
        self.period_type = period_type
        self.period_count = period_count
        self.constituents = constituents
        self.href = href
        self.links = links
