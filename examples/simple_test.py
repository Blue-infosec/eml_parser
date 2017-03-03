#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
from __future__ import absolute_import, division, print_function, unicode_literals

#
# Georges Toth (c) 2013-2014 <georges@trypill.org>
# GOVCERT.LU (c) 2013-2017 <info@govcert.etat.lu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import json
import argparse
import datetime
import eml_parser


__author__ = 'Toth Georges, Jung Paul'
__email__ = 'georges@trypill.org, georges.toth@govcert.etat.lu'
__copyright__ = 'Copyright 2013-2014 Georges Toth, Copyright 2013-2017 GOVCERT Luxembourg'
__license__ = 'AGPL v3+'


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial

    raise TypeError("Type not serializable")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i', dest='msgfile',
                        help='input file', required=True)
    parser.add_argument('-d', dest='debug', action='store_true',
                        help='debug (no hashing)')
    parser.add_argument('-r', dest='fulldata', action='store_true',
                        help='includes raw data of attachments')
    parser.add_argument('-w', dest='whitelist_ip',
                        help='whitelist IPv4 or IPv6 ip from parsing; comma-separated list of IPs, no spaces !')
    parser.add_argument('-f', dest='whitelist_email',
                        help='whitelist an email in routing headers "For"; comma-separated list of e-mail addresses, no spaces !')
    parser.add_argument('-b', dest='byhostentry',
                        help='collect the smtp injector IP using the "by" "host" in routing headers; comma-separated list of IPs, no spaces !')

    options = parser.parse_args()

    msgfile = options.msgfile
    full = options.debug
    fulldata = options.fulldata
    pconf = {}

    if options.whitelist_ip is not None:
        pconf['whiteip'] = options.whitelist_ip.split(',')

    if options.whitelist_email is not None:
        pconf['whitefor'] = options.whitelist_email.split(',')

    if options.byhostentry is not None:
        pconf['byhostentry'] = options.byhostentry.split(',')

    m = eml_parser.decode_email(msgfile, full, fulldata, pconf)
    print (json.dumps(m, default=json_serial))


if __name__ == '__main__':
    main()
