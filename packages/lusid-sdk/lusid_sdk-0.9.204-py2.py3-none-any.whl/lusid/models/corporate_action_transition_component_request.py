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


class CorporateActionTransitionComponentRequest(Model):
    """CorporateActionTransitionComponentRequest.

    :param instrument_identifiers: unique instrument identifiers.
    :type instrument_identifiers: dict[str, str]
    :param units_factor:
    :type units_factor: float
    :param cost_factor:
    :type cost_factor: float
    """

    _validation = {
        'instrument_identifiers': {'required': True},
        'units_factor': {'required': True},
        'cost_factor': {'required': True},
    }

    _attribute_map = {
        'instrument_identifiers': {'key': 'instrumentIdentifiers', 'type': '{str}'},
        'units_factor': {'key': 'unitsFactor', 'type': 'float'},
        'cost_factor': {'key': 'costFactor', 'type': 'float'},
    }

    def __init__(self, instrument_identifiers, units_factor, cost_factor):
        super(CorporateActionTransitionComponentRequest, self).__init__()
        self.instrument_identifiers = instrument_identifiers
        self.units_factor = units_factor
        self.cost_factor = cost_factor
