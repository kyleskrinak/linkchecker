# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004-2012 Bastian Kleineidam
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
Test mail checking.
"""
from tests import need_network
from . import MailTest


class TestMailGood (MailTest):
    """
    Test mailto: link checking.
    """

    @need_network
    def test_good_mail (self):
        # some good mailto addrs
        url = self.norm(u"mailto:Dude <calvin@users.sourceforge.net> , "\
                "Killer <calvin@users.sourceforge.net>?subject=bla")
        resultlines = [
          u"url %s" % url,
          u"cache key mailto:calvin@users.sourceforge.net",
          u"real url %s" % url,
          u"info Verified address calvin@users.sourceforge.net: 250 <calvin@users.sourceforge.net> is deliverable.",
          u"valid",
        ]
        self.direct(url, resultlines)
        url = self.norm(u"mailto:Bastian Kleineidam <calvin@users.sourceforge.net>?"\
                "bcc=calvin%40users.sourceforge.net")
        resultlines = [
          u"url %s" % url,
          u"cache key mailto:calvin@users.sourceforge.net",
          u"real url %s" % url,
          u"info Verified address calvin@users.sourceforge.net: 250 <calvin@users.sourceforge.net> is deliverable.",
          u"valid",
        ]
        self.direct(url, resultlines)
        url = self.norm(u"mailto:Bastian Kleineidam <calvin@users.sourceforge.net>")
        resultlines = [
            u"url %s" % url,
            u"cache key mailto:calvin@users.sourceforge.net",
            u"real url %s" % url,
            u"info Verified address calvin@users.sourceforge.net: 250 <calvin@users.sourceforge.net> is deliverable.",
            u"valid",
        ]
        self.direct(url, resultlines)
        url = self.norm(u"mailto:o'hara@users.sourceforge.net")
        resultlines = [
            u"url %s" % url,
            u"cache key mailto:o'hara@users.sourceforge.net",
            u"real url %s" % url,
            u"warning Unverified address: 550 <o'hara@users.sourceforge.net> Unrouteable address.",
            u"valid",
        ]
        self.direct(url, resultlines)
        url = self.norm(u"mailto:?to=calvin@users.sourceforge.net&subject=blubb&"
                       u"cc=calvin_cc@users.sourceforge.net&CC=calvin_CC@users.sourceforge.net")
        resultlines = [
            u"url %s" % url,
            u"cache key mailto:calvin@users.sourceforge.net,"
             u"calvin_CC@users.sourceforge.net,calvin_cc@users.sourceforge.net",
            u"real url %s" % url,
           u"info Verified address calvin@users.sourceforge.net: 250 <calvin@users.sourceforge.net> is deliverable.",
            u"warning Unverified address: 550 <calvin_CC@users.sourceforge.net> Unrouteable address.",
            u"warning Unverified address: 550 <calvin_cc@users.sourceforge.net> Unrouteable address.",
            u"valid",
        ]
        self.direct(url, resultlines)
        url = self.norm(u"mailto:news-admins@freecode.com?subject="
                "Re:%20[fm%20#11093]%20(news-admins)%20Submission%20"
                "report%20-%20Pretty%20CoLoRs")
        resultlines = [
            u"url %s" % url,
            u"cache key mailto:news-admins@freecode.com",
            u"real url %s" % url,
            u"warning Unverified address: 502 5.5.1 VRFY command is disabled.",
            u"valid",
        ]
        self.direct(url, resultlines)

    @need_network
    def test_warn_mail (self):
        # some mailto addrs with warnings
        # contains non-quoted characters
        url = u"mailto:calvin@users.sourceforge.net?subject=���"
        qurl = self.norm(url)
        resultlines = [
            u"url %s" % url,
            u"cache key mailto:calvin@users.sourceforge.net",
            u"real url %s" % qurl,
            u"info Verified address calvin@users.sourceforge.net: 250 <calvin@users.sourceforge.net> is deliverable.",
            u"valid",
        ]
        self.direct(url, resultlines)
        url = u"mailto:calvin@users.sourceforge.net?subject=Halli hallo"
        qurl = self.norm(url)
        resultlines = [
            u"url %s" % url,
            u"cache key mailto:calvin@users.sourceforge.net",
            u"real url %s" % qurl,
            u"info Verified address calvin@users.sourceforge.net: 250 <calvin@users.sourceforge.net> is deliverable.",
            u"valid",
        ]
        self.direct(url, resultlines)
        url = u"mailto:"
        resultlines = [
            u"url %s" % url,
            u"cache key mailto:",
            u"real url %s" % url,
            u"warning No mail addresses found in `%s'." % url,
            u"valid",
        ]
        self.direct(url, resultlines)

    def _mail_valid_unverified(self, char):
        # valid mail addresses
        addr = u'abc%sdef@sourceforge.net' % char
        url = u"mailto:%s" % addr
        self.mail_valid(url,
          warning=u"Unverified address: 550 <%s> Unrouteable address." % addr,
          cache_key=url)

    @need_network
    def test_valid_mail1 (self):
        for char in u"!#$&'":
            self._mail_valid_unverified(char)

    @need_network
    def test_valid_mail2 (self):
        for char in u"*+-/=":
            self._mail_valid_unverified(char)

    @need_network
    def test_valid_mail3 (self):
        for char in u"^_`.":
            self._mail_valid_unverified(char)

    @need_network
    def test_valid_mail4 (self):
        for char in u"{|}~":
            self._mail_valid_unverified(char)

    @need_network
    def test_unicode_mail (self):
        mailto = u"mailto:�lvin@users.sourceforge.net"
        url = self.norm(mailto, encoding="iso-8859-1")
        resultlines = [
            u"url %s" % url,
            u"cache key %s" % mailto,
            u"real url %s" % url,
            u"warning Unverified address: 550 <lvin@users.sourceforge.net> Unrouteable address.",
            u"valid",
        ]
        self.direct(url, resultlines)
