# -*- coding: UTF-8 -*-
# Copyright 2016 Rumma & Ko Ltd
# This file is part of Lino Welfare.
#
# Lino Welfare is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Welfare is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Welfare.  If not, see
# <http://www.gnu.org/licenses/>.
"""
Standard data for `lino_welfare.modlib.esf`.
"""

from lino.api import dd, rt, _


def objects():

    ExcerptType = rt.models.excerpts.ExcerptType
    kw = dict(
        build_method='weasy2pdf',
        certifying=True)
    kw.update(dd.str2kw('name', _("Training report")))
    yield ExcerptType.update_for_model('esf.ClientSummary', **kw)
