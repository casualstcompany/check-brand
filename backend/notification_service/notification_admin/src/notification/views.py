from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from jinja2 import Template

from notification.models import TemplateMail


def template_detail(request, id):
    obj = get_object_or_404(TemplateMail, id=id)
    template = Template(obj.body_html)
    return HttpResponse(template.render(**obj.payload))
