# -*- coding: UTF-8 -*-
# Copyright 2012-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Adds functionality to make CBSS requests.

Technical specs see :ref:`weleup`.

.. autosummary::
   :toctree:

    mixins
    choicelists
    utils
    fixtures.cbss_demo
    fixtures.cbss
    fixtures.purposes
    fixtures.sectors

.. rubric:: Plugin configuration

"""

from lino import ad
from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    """The descriptor for this plugin. See
    :class:`lino.core.plugin.Plugin`.

    """
    verbose_name = _("CBSS")

    needs_plugins = ['lino_welfare.modlib.integ']

    cbss_live_requests = False
    """Whether executing requests should try to really connect to the
    CBSS.  Real requests would fail with a timeout if run from behind
    an IP address that is not registered at the :term:`CBSS`.

    """

    #~ cbss_environment = None
    cbss_environment = 'test'
    """
    Either `None` or one of 'test', 'acpt' or 'prod'.
    
    Setting this to `None` means that the cbss app is "inactive" even
    if installed.

    """

    def get_used_libs(self, html=None):
        try:
            import suds
            version = suds.__version__
        except ImportError:
            version = self.site.not_found_msg
        yield ("suds", version, "https://fedorahosted.org/suds/")

    def setup_main_menu(self, site, user_type, m):
        mg = site.plugins.integ
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('cbss.MyIdentifyPersonRequests')
        m.add_action('cbss.MyManageAccessRequests')
        m.add_action('cbss.MyRetrieveTIGroupsRequests')

    def setup_config_menu(self, site, user_type, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('cbss.Sectors')
        m.add_action('cbss.Purposes')

    def setup_explorer_menu(self, site, user_type, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('cbss.AllIdentifyPersonRequests')
        m.add_action('cbss.AllManageAccessRequests')
        m.add_action('cbss.AllRetrieveTIGroupsRequests')

