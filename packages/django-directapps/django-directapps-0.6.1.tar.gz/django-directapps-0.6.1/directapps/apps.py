# -*- coding: utf-8 -*-
#
#   Copyright 2016 Grigoriy Kramarenko <root@rosix.ru>
#
#   This file is part of DirectApps.
#
#   DirectApps is free software: you can redistribute it and/or
#   modify it under the terms of the GNU Affero General Public License
#   as published by the Free Software Foundation, either version 3 of
#   the License, or (at your option) any later version.
#
#   DirectApps is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public
#   License along with DirectApps. If not, see
#   <http://www.gnu.org/licenses/>.
#

from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _


class AppConfig(BaseAppConfig):
    name = 'directapps'
    verbose_name = _('Direct Apps')
