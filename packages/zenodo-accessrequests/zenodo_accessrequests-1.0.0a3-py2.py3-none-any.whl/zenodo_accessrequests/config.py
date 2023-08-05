# -*- coding: utf-8 -*-
#
# This file is part of Zenodo.
# Copyright (C) 2015, 2016 CERN.
#
# Zenodo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Zenodo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Zenodo. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""Default configuration values."""

from __future__ import absolute_import, print_function

ACCESSREQUESTS_CONFIRMLINK_EXPIRES_IN = 5*24*60*60
"""Number of seconds after the email confirmation link expires."""

ACCESSREQUESTS_RECORDS_UI_ENDPOINTS = dict(
    recid_access_request=dict(
        pid_type='recid',
        route='/record/<pid_value>/accessrequest',
        template='zenodo_accessrequests/access_request.html',
        view_imp='zenodo_accessrequests.views.requests.access_request',
        methods=['GET', 'POST'],
    ),
    recid_access_request_email_confirm=dict(
        pid_type='recid',
        route='/record/<pid_value>/accessrequest/<token>/confirm',
        view_imp='zenodo_accessrequests.views.requests.confirm',
    ),
)
