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


class PropertyValue(Model):
    """PropertyValue.

    :param label_value:
    :type label_value: str
    :param metric_value:
    :type metric_value: ~lusidtr.models.MetricValue
    :param effective_from: Date for which the property is effective from
    :type effective_from: datetime
    """

    _attribute_map = {
        'label_value': {'key': 'labelValue', 'type': 'str'},
        'metric_value': {'key': 'metricValue', 'type': 'MetricValue'},
        'effective_from': {'key': 'effectiveFrom', 'type': 'iso-8601'},
    }

    def __init__(self, label_value=None, metric_value=None, effective_from=None):
        super(PropertyValue, self).__init__()
        self.label_value = label_value
        self.metric_value = metric_value
        self.effective_from = effective_from
