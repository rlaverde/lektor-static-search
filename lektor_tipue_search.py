# -*- coding: utf-8 -*-
import os
import json
from collections import defaultdict

from lektor.reporter import reporter
from lektor.pluginsystem import Plugin
from lektor.db import Page


class TipueSearchPlugin(Plugin):
    name = u'Lektor Tipue Search'
    description = u'Serialize models contents for using tipue search.'

    def __init__(self, *args, **kwargs):
        Plugin.__init__(self, *args, **kwargs)
        self.tipue_search = defaultdict(list)
        self.enabled = False

    def check_enabled(func):
        def func_wrapper(self, *args, **kwargs):
            if not self.enabled:
                return
            func(self, *args, **kwargs)

        return func_wrapper

    def on_server_spawn(self, **extra):
        extra_flags = extra.get("extra_flags") \
                      or extra.get("build_flags") or {}
        self.enabled = bool(extra_flags.get('tipue'))

    def on_setup_env(self, **extra):
        #TODO load configurations
        pass

    @check_enabled
    def on_before_build_all(self, builder, **extra):
        self.tipue_search.clear()

        self.output_path = 'tipue_search'

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    @check_enabled
    def on_before_build(self, source, prog, **extra):
        if isinstance(source, Page):
            #FIXME at the moment only support blog-post
            if source.datamodel.id == 'blog-post':
                item = {'title': source['title'],
                        'text': source['summary'],
                        'tags': source['tags'], }

                self.tipue_search[source.alt].append(item)

    @check_enabled
    def on_after_build_all(self, builder, **extra):
        for alt, pages in self.tipue_search.items():
            filename = os.path.join(builder.env.root_path, self.output_path,
                                    'tipue_search_{}.json'.format(alt))

            try:
                with open(filename, 'r') as f:
                    contents = f.read()
            except IOError:
                contents = ""

            if contents != json.dumps(pages):
                with open(filename, 'w') as f:
                    f.write(json.dumps(pages))

                reporter.report_generic('generated tipue search file{}'.format(
                    filename))
