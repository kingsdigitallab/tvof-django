# -*- coding: utf-8 -*-
from django.shortcuts import render
import utils as dputils
from datetime import datetime
from pattern_analyser import PatternAnalyser
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def patterns_view(request, slug):
    ana = PatternAnalyser(slug)
    context = ana.process_request_html(request)
    template = 'text_patterns/patterns.html'
    ret = render(request, template, context)
    return ret


@csrf_exempt
def patterns_api_view(request, slug, root, path):
    ana = PatternAnalyser(slug)
    data = ana.process_request_api(request, root, path)
    format = data.get('format', 'json')
    if format in ['csv']:
        now = datetime.now()
        file_name = 'segments-%s-%s-%s.csv' % (now.day, now.month, now.year)
        ret = dputils.get_csv_response_from_rows(data['csv'], headings=[
            'unitid', 'pattern_group',
            'pattern_key', 'segment', 'variant'], filename=file_name)
    else:
        ret = dputils.get_json_response(data)
    return ret
