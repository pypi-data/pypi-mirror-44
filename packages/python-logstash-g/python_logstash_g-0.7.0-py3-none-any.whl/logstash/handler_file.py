# coding: utf-8
from __future__ import unicode_literals

import sys

from logging.handlers import RotatingFileHandler
from logstash.mixins import ConfigFormatterClassMixin


class FileLogstashHandler(ConfigFormatterClassMixin, RotatingFileHandler, object):
    """
    Python logging handler for Logstash.
    Write log into disk files.
    """

    def __init__(self, *args, **kwargs):
        super(FileLogstashHandler, self).__init__(kwargs['filename'],
                                                  mode=kwargs.get('mode', 'a'),
                                                  maxBytes=kwargs.get('maxBytes', 0),
                                                  backupCount=kwargs.get('backupCount',
                                                                         0),
                                                  encoding=kwargs.get('encoding', None),
                                                  delay=kwargs.get('delay', 0))
        message_type = kwargs.get('message_type', 'logstash')
        tags = kwargs.get('tags', None)
        fqdn = kwargs.get('fqdn', False)
        version = kwargs.get('version', 0)
        formatter_path = kwargs.get('formatter_path', None)
        self.config_formatter(
            message_type=message_type,
            tags=tags,
            fqdn=fqdn,
            version=version,
            class_path=formatter_path,
        )

    def format(self, record):
        msg = super(FileLogstashHandler, self).format(record)
        if sys.version_info > (3, 0):
            msg = bytes.decode(msg)
        return msg
