#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2010-2019 Etienne Robillard <tkadm30@yandex.com>
# All rights reserved.
from notmm.dbapi.orm import decorators
from notmm.utils.template import direct_to_template
#from notmm.utils.cache import cached
__all__ = ('index',)

# dicts in python are expensives, so they must be cached
#@cached
@decorators.with_schevo_database('127.0.0.1:4545')
def index(request, available_templates={'en': 'blogengine2/index.mako'}, 
    response_callback=direct_to_template, **kwargs):
    db = request.environ['schevo.db.zodb']
    # get the list of messages
    messages = db.Message.find()
    messages.reverse()
    #db.close()
    if not 'template_name' in kwargs:
        template = available_templates[request.environ.get('django.i18n.charset', 'en')]
    else:
        template = kwargs['template_name']
    extra_context = {'messages': messages}    
    return response_callback(request, template, extra_context=extra_context)


