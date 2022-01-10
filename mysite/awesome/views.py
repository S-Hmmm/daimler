from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django import forms
import json

from .models import Cases


def index(request):
    case_list = Cases.objects.all()
    context = {
        'case_list': case_list
    }
    return render(request, 'awesome/index.html', context)


def detail(request, case_id):
    case = get_object_or_404(Cases, id=case_id)
    return render(request, 'awesome/detail.html', context={'case': case})


class PtForm(forms.Form):
    case_name = forms.CharField(label='用例名称', min_length=2, max_length=10)
    method = forms.CharField(label='请求方法', max_length=6)


def pt(request):
    if request.method == 'POST':
        form = PtForm(request.POST)
        print(request.POST['case_name'])
        if form.is_valid():
            return HttpResponse('请求成功')
    else:
        form = PtForm()
    return render(request, 'awesome/pt.html', locals())


@require_http_methods(['GET'])
def node(request):
    resp = {}
    try:
        resp['cases'] = json.loads(serializers.serialize('json', Cases.objects.filter(method='get')))
        resp['status_code'] = 0
    except Exception as e:
        resp['error_msg'] = e
        resp['status_code'] = 1
    return JsonResponse(resp)
