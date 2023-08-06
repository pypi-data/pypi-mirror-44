# coding=utf-8
# --------------------------------------------------------------------------
# Copyright © 2018 FINBOURNE TECHNOLOGY LTD
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


class AggregationContext(Model):
    """Aggregation context node. Whilst the market and pricing nodes concern
    themselves with which models are used and where the market data comes from,
    the aggregation
    context determines how data is aggregated together. This controls the
    behaviour of the grouping and sql-like engine at the back of the valuation.
    For instance,
    it controls conversion of currencies and whether the sql-like engine
    behaves more like ANSI or MySql SQL.

    :param options: Miscellaneous options for controlling aggregation.
    :type options: ~lusid.models.AggregationOptions
    """

    _attribute_map = {
        'options': {'key': 'options', 'type': 'AggregationOptions'},
    }

    def __init__(self, options=None):
        super(AggregationContext, self).__init__()
        self.options = options
