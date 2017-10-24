#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections.abc import Iterable
from wtforms.widgets import html_params


class FileDisplayWidget(object):
    html_params = staticmethod(html_params)

    def __init__(self, input_type='string', text=''):
        self.input_type = input_type
        self.text = text

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = [u'<ul %s>' % html_params(id=field.id)]
        data = field.data
        if not isinstance(data, Iterable):
            params = dict(kwargs, href=data)
            html.append(u'<li><a %s>%s</li>' % (html_params(**params), data))
        else:
            for link in data:
                params = dict(kwargs, href=link)
                html.append(u'<li ><a %s>%s</li>' % (html_params(**params), link))
        html.append(u'</ul>')
        return u''.join(html)
