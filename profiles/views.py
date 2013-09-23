from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.functional import lazy



@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return HttpResponseRedirect(reverse('core:home'))


def private(request):
    return TemplateResponse(request, 'users/private.html', None)
