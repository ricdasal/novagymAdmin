import datetime
from urllib.parse import urlparse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin, PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.db.models.aggregates import Count
from django.http.response import JsonResponse
from django.shortcuts import render, resolve_url
from django.utils import timezone

from .models import *

# Admin.


class PersonalPermissionRequieredMixin(PermissionRequiredMixin, AccessMixin):
    raise_exception = False

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        path = self.request.build_absolute_uri()
        resolved_login_url = resolve_url(self.get_login_url())
        # If the login url is the same scheme and net location then use the
        # path as the "next" url.
        login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
        current_scheme, current_netloc = urlparse(path)[:2]
        if (
            (not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)
        ):
            path = self.request.get_full_path()
        return redirect_to_login(
            path,
            resolved_login_url,
            self.get_redirect_field_name(),
        )


def daterange(start_date, end_date):
    """
    Generetor to return dates from start_date to end_date.
    
    i.e start_date: 05/03/2022 end_date: 08/03/2022
    
    each iteration will return 05/03/20222, 06/03/2022, ...
    
    08/03/2022


    Args:
        start_date (datetime): start date for the generator
        end_date (datetime): end date for the generator
    """
    for n in range(int((end_date - start_date).days+1)):
        yield start_date + datetime.timedelta(n)
