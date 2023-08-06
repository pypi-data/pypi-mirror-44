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

from __future__ import unicode_literals
import json
from hashlib import md5

from django.apps import apps as django_apps
from django.http import (HttpResponseBadRequest, HttpResponseForbidden,
                         HttpResponseNotFound, HttpResponseServerError)
from django.core.exceptions import (FieldError, PermissionDenied,
                                    ValidationError as DjangoValidationError)
from django.core.paginator import EmptyPage
from django.urls import reverse
from django.utils import six
from django.utils.encoding import force_text, force_bytes
from django.utils.translation import ugettext_lazy as _

from directapps import __version__
from directapps.conf import (access, EXCLUDE_APPS, EXCLUDE_MODELS,
                             JSON_DUMPS_PARAMS, CHECKSUM_VERSION)
from directapps.controllers import get_controller
from directapps.decorators import parse_rest
from directapps.encoders import JSONEncoder
from directapps.exceptions import ValidationError, NotExistError
from directapps.response import JsonResponse
from directapps.utils import get_model_perms, has_model_perms, is_m2m_layer


@parse_rest
def director(request, app=None, model=None, **kwargs):
    """
    Главный распределитель запросов к моделям приложений.

    В `kwargs` могут быть: object, relation, relation_object и action.
    """
    user = request.user
    is_auth = user.is_authenticated
    if callable(is_auth):
        is_auth = is_auth()
    if not is_auth:
        return HttpResponseBadRequest(_("You need to login."), status=401)
    if not access(request):
        return HttpResponseForbidden(_("You don't have access to this page."))
    if app:
        if not user.has_module_perms(app):
            return HttpResponseForbidden(
                _("You don't have access to this application.")
            )
        if app in EXCLUDE_APPS:
            return HttpResponseBadRequest(_('Application is disabled.'))
        try:
            app = django_apps.get_app_config(app)
        except LookupError:
            return HttpResponseNotFound(_('Application not found.'))
        if model:
            fullname = '%s.%s' % (app.label, model)
            if model not in app.models:
                return HttpResponseNotFound(_('Model not found.'))
            if fullname in EXCLUDE_MODELS:
                return HttpResponseBadRequest(_('Model is disabled.'))
            model = app.models[model]
            if not has_model_perms(user, model):
                return HttpResponseForbidden(
                    _("You don't have access to this model.")
                )
            try:
                ctrl = get_controller(model)
                data = ctrl.routing(request, **kwargs)
            except NotExistError as e:
                return HttpResponseNotFound(force_text(e))
            except (FieldError, ValidationError) as e:
                return HttpResponseBadRequest(force_text(e))
            except DjangoValidationError as e:
                return HttpResponseBadRequest('\n'.join(e.messages))
            except PermissionDenied:
                return HttpResponseForbidden(
                    _("You don't have access to this action.")
                )
            except (IndexError, model.DoesNotExist, EmptyPage):
                return HttpResponseNotFound(_('Object not found.'))
            except (TypeError, ValueError) as e:
                return HttpResponseBadRequest(force_text(e))
            except NotImplementedError:
                return HttpResponseServerError(_('Not implemented.'))
        else:
            # Возвращаем схему приложения, включая полные схемы моделей
            data = get_scheme_app(request, app, True)
    else:
        # Возвращаем общую схему всех приложений "первого уровня".
        # То есть, исключая полные схемы моделей внутри каждого приложения.
        data = get_scheme_apps(request)

    return JsonResponse(data, safe=False, json_dumps_params=JSON_DUMPS_PARAMS)


def version(request):
    data = {
        'checksum': CHECKSUM_VERSION,
        'directapps': __version__,
    }
    return JsonResponse(data, json_dumps_params=JSON_DUMPS_PARAMS)


def get_scheme_model(request, model, full):
    """Возвращает полную или неполную схему модели."""
    user = request.user
    if has_model_perms(user, model):
        meta = model._meta
        M = {
            'name': meta.model_name,
            'display_name': force_text(meta.verbose_name_plural),
            'url': reverse('directapps:model',
                           args=(meta.app_label, meta.model_name))
        }
        if user.is_superuser:
            M['perms'] = 'all'
        else:
            M['perms'] = list(get_model_perms(user, model))
        if full:
            M.update(get_controller(model).get_scheme(request))
        return M
    return None


def get_scheme_app(request, app, include_model_schemes):
    """Возвращает полную или неполную схему приложения."""
    user = request.user
    if user.has_module_perms(app.label):
        models = []
        A = {
            'name': app.label,
            'display_name': force_text(app.verbose_name),
            'models': models,
            'url': reverse('directapps:app', args=(app.label,)),
            'complete': include_model_schemes
        }
        for model_name, model in six.iteritems(app.models):
            if is_m2m_layer(model):
                continue
            meta = model._meta
            if meta.swapped or meta.abstract:
                continue
            fullname = '%s.%s' % (app.label, model_name)
            if fullname in EXCLUDE_MODELS:
                continue
            M = get_scheme_model(request, model, full=include_model_schemes)
            if M:
                models.append(M)
        if models:
            return A
    return None


def get_scheme_apps(request):
    """
    Возвращает общую схему "первого уровня" для всех доступных
    приложений.
    """
    data = []
    for app in django_apps.get_app_configs():
        if app.label in EXCLUDE_APPS:
            continue
        A = get_scheme_app(request, app, False)
        if A:
            data.append(A)
    cs = md5(force_bytes(CHECKSUM_VERSION))
    cs.update(force_bytes(__version__))
    cs.update(force_bytes(json.dumps(data, cls=JSONEncoder)))
    return {
        'checksum': cs.hexdigest(),
        'version': __version__,
        'apps': data
    }
