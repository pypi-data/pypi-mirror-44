#!/usr/bin/python
# Copyright (C) 2019 Jelmer Vernooij
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
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

from breezy.tests import TestCaseWithTransport

from ..proposal import (
    push_result,
    )


class PushResultTests(TestCaseWithTransport):

    def test_simple(self):
        target = self.make_branch('target')
        source = self.make_branch_and_tree('source')
        revid = source.commit('Some change')
        push_result(source.branch, target)
        self.assertEqual(target.last_revision(), revid)
