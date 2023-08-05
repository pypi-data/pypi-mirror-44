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

"""Signal receivers."""

from __future__ import absolute_import, print_function

from datetime import timedelta

from flask import current_app, render_template, url_for
from flask_babelex import gettext as _
from flask_mail import Message
from invenio_mail.tasks import send_email

from .errors import RecordNotFound
from .signals import request_accepted, request_confirmed, request_created, \
    request_rejected
from .tokens import EmailConfirmationSerializer
from .utils import get_record


def connect_receivers():
    """Connect receivers to signals."""
    request_created.connect(send_email_validation)
    request_confirmed.connect(send_confirmed_notifications)
    request_rejected.connect(send_reject_notification)
    # Order is important:
    request_accepted.connect(create_secret_link)
    request_accepted.connect(send_accept_notification)


def create_secret_link(request, message=None, expires_at=None):
    """Receiver for request-accepted signal."""
    pid, record = get_record(request.recid)
    if not record:
        raise RecordNotFound(request.recid)

    description = render_template(
        "zenodo_accessrequests/link_description.tpl",
        request=request,
        record=record,
        pid=pid,
        expires_at=expires_at,
        message=message,
    )

    request.create_secret_link(
        record["title"],
        description=description,
        expires_at=expires_at
    )


def send_accept_notification(request, message=None, expires_at=None):
    """Receiver for request-accepted signal to send email notification."""
    pid, record = get_record(request.recid)
    _send_notification(
        request.sender_email,
        _("Access request accepted"),
        "zenodo_accessrequests/emails/accepted.tpl",
        request=request,
        record=record,
        pid=pid,
        record_link=request.link.get_absolute_url('invenio_records_ui.recid'),
        message=message,
        expires_at=expires_at,
    )


def send_confirmed_notifications(request):
    """Receiver for request-confirmed signal to send email notification."""
    pid, record = get_record(request.recid)
    if record is None:
        current_app.logger.error("Cannot retrieve record %s. Emails not sent"
                                 % request.recid)
        return
    title = _("Access request: %(record)s", record=record["title"])

    _send_notification(
        request.receiver.email,
        title,
        "zenodo_accessrequests/emails/new_request.tpl",
        request=request,
        record=record,
        pid=pid,
    )

    _send_notification(
        request.sender_email,
        title,
        "zenodo_accessrequests/emails/confirmation.tpl",
        request=request,
        record=record,
        pid=pid,
    )


def send_email_validation(request):
    """Receiver for request-created signal to send email notification."""
    token = EmailConfirmationSerializer().create_token(
        request.id, dict(email=request.sender_email)
    )
    pid, record = get_record(request.recid)

    _send_notification(
        request.sender_email,
        _("Access request verification"),
        "zenodo_accessrequests/emails/validate_email.tpl",
        request=request,
        record=record,
        pid=pid,
        days=timedelta(
            seconds=current_app.config["ACCESSREQUESTS_CONFIRMLINK_EXPIRES_IN"]
        ).days,
        confirm_link=url_for(
            "invenio_records_ui.recid_access_request_email_confirm",
            pid_value=request.recid,
            token=token,
            _external=True,
        )
    )


def send_reject_notification(request, message=None):
    """Receiver for request-rejected signal to send email notification."""
    pid, record = get_record(request.recid)
    _send_notification(
        request.sender_email,
        _("Access request rejected"),
        "zenodo_accessrequests/emails/rejected.tpl",
        request=request,
        record=record,
        pid=pid,
        message=message,
    )


def _send_notification(to, subject, template, **ctx):
    """Render a template and send as email."""
    msg = Message(
        subject,
        sender=current_app.config.get('SUPPORT_EMAIL'),
        recipients=[to]
    )
    msg.body = render_template(template, **ctx)

    send_email.delay(msg.__dict__)
