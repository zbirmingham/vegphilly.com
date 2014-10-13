# Copyright (C) 2013 Steve Lamb

# This file is part of Vegancity.

# Vegancity is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Vegancity is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Vegancity.  If not, see <http://www.gnu.org/licenses/>.

""" A simple module for sending emails through gmail """

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string

from vegancity.models import User


def send_new_vendor_approval(vendor):
    subject = '[VegPhilly] New Vendor Approved'
    html_body = render_to_string(
        "vegancity/approval_email.html", {'vendor': vendor})
    text_body = strip_tags(html_body)
    sender = settings.EMAIL_HOST_USER
    recipients = [vendor.submitted_by.email]

    msg = EmailMultiAlternatives(subject,
                                 text_body,
                                 sender,
                                 recipients)

    msg.attach_alternative(html_body, "text/html")
    msg.send(fail_silently=True)


def send_new_vendor_alert(vendor):
    subject = '[VegPhilly] New Vendor Submitted'
    html_body = render_to_string(
        'vegancity/new_vendor_alert_email.html', {'vendor': vendor})
    text_body = strip_tags(html_body)
    sender = settings.EMAIL_HOST_USER
    recipients = [user.email for user in User.objects.filter(is_staff=True)]

    msg = EmailMultiAlternatives(subject,
                                 text_body,
                                 sender,
                                 recipients)

    msg.attach_alternative(html_body, 'text/html')
    msg.send(fail_silently=True)
