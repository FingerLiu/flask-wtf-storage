#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.parse import unquote

from collections.abc import Iterable
from wtforms.widgets import html_params, HTMLString


class FileDisplayWidget(object):

    def __init__(self, input_type='string', text=''):
        self.input_type = input_type
        self.text = text

    def get_filename(self, name):
        # return '-'.join(name.split('/')[-1].split('-')[1:])
        return '-'.join(name.split())

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = [u'<ul %s>' % html_params(id=field.id)]
        data = field.data
        if data:
            if not isinstance(data, Iterable):
                data = unquote(data)
                params = dict(href=data)
                html.append(u'<li><a target="_blank" %s>%s</a></li>' % (html_params(**params), self.get_filename(data)))
            else:
                for link in data:
                    if link:
                        link = unquote(link)
                        params = dict(href=link)
                        html.append(u'<li ><a target="_blank" %s>%s</a></li>' % (html_params(**params), self.get_filename(link)))
        html.append(u'</ul>')
        return HTMLString(u''.join(html))
