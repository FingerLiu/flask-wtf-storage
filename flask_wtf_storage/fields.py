#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import current_app
from wtforms import widgets
from wtforms import Field
from werkzeug.datastructures import FileStorage
from flask_wtf.file import FileField as _FileField

from .widgets import FileDisplayWidget
from .utils import upload_file, upload_file2local


class FileInput(widgets.Input):
    input_type = 'file'

    def __init__(self, multiple=False):
        super().__init__()
        self.multiple = multiple

    def __call__(self, field, **kwargs):
        # browser ignores value of file input for security
        kwargs['value'] = False

        if self.multiple:
            kwargs['multiple'] = True

        return super().__call__(field, **kwargs)


class FileField(_FileField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage_engine = current_app.config.get('STORAGE_ENGINE', 'GOOGLE_STORAGE')

    def upload(self):
        current_app.logger.info('start upload FileField %s', self.name)
        if self.storage_engine == 'GOOGLE_STORAGE':
            stream = self.data.stream.read()
            if stream:
                upload_name = '%s/%s' % (self.name, self.data.filename)
                url = upload_file(upload_name, stream)
                return url
            else:
                return None
        elif self.storage_engine == 'LOCAL':
            return upload_file2local(self.data)
        else:
            raise NotImplementedError


class CustomFileField(FileField):
    def _value(self):
        return False


class MultipleFileField(CustomFileField):
    widget = FileInput(multiple=True)

    def process_formdata(self, valuelist):
        valuelist = [x for x in valuelist if isinstance(x, FileStorage) and x]
        self.data = valuelist

    def upload(self):
        current_app.logger.info('start upload MultipleFileField %s', self.name)
        storage_engine = current_app.config.get('STORAGE_ENGINE', 'GOOGLE_STORAGE')
        # current_app.logger.info('data %s', self.data)
        if storage_engine == 'GOOGLE_STORAGE':
            data = self.data
            if not data:
                return []
            names = []
            for f in data:
                current_app.logger.debug('f in data %s', f.filename)
                stream = f.stream.read()
                if stream:
                    upload_name = '%s/%s' % (self.name, f.filename)
                    name = upload_file(upload_name, stream)
                    names.append(name)
            return names
        elif storage_engine == 'LOCAL':
            data = self.data
            if not data:
                return []
            names = []
            for f in data:
                current_app.logger.debug('f in data %s', f.filename)
                names.append(upload_file2local(f))
            return names

        else:
            raise NotImplementedError


class FileDisplayField(Field):
    widget = FileDisplayWidget()
