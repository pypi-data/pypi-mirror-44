# Copyright 2013-2016 Rumma & Ko Ltd
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
Lino Welfare extension of :mod:`lino_xl.lib.cal`

.. autosummary::
   :toctree:

    fixtures.std
    fixtures.demo
    fixtures.demo2



"""

from lino_xl.lib.cal import Plugin


class Plugin(Plugin):
    """See :class:`lino.core.plugin.Plugin`."""

    extends_models = ['Event', 'EventType', 'Guest', 'Task']

    partner_model = 'contacts.Partner'
