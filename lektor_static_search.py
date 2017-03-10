# -*- coding: utf-8 -*-
import os
import json
from collections import defaultdict
from jinja2 import Undefined

from lektor.reporter import reporter
from lektor.pluginsystem import Plugin
from lektor.db import Page


class StaticSearchPlugin(Plugin):
    name = u'Lektor Static Search'
    description = u'Serialize models contents for using with static search js libraries.'

    def __init__(self, *args, **kwargs):
        Plugin.__init__(self, *args, **kwargs)
        self.static_search = defaultdict(list)
        self.enabled = False
        self.models = None
        self.options = {'output_path': 'static-search', }

    def check_enabled(func):
        def func_wrapper(self, *args, **kwargs):
            if not self.enabled:
                return
            func(self, *args, **kwargs)

        return func_wrapper

    def on_server_spawn(self, **extra):
        extra_flags = extra.get("extra_flags") \
                      or extra.get("build_flags") or {}
        self.enabled = bool(extra_flags.get('static-search'))

    def on_setup_env(self, **extra):
        self.models = defaultdict(dict)

        for key, item in self.get_config().items():
            config_option = key.split('.')

            # Load models configurations
            if config_option[0] == 'model':
                model, field = config_option[1:]
                self.models[model][field] = item

        for option in self.options.keys():
            value = self.get_config().get(option)

            if value is not None:
                self.options[option] = value

    @check_enabled
    def on_before_build_all(self, builder, **extra):
        self.static_search.clear()

        output_path = os.path.join(builder.env.root_path,
                                   self.options['output_path'])
        if not os.path.exists(output_path):
            os.makedirs(output_path)

    @check_enabled
    def on_before_build(self, source, prog, **extra):
        if isinstance(source, Page):

            if source.datamodel.id in self.models:
                model = self.models[source.datamodel.id]

                item = {key: None if isinstance(source[field], Undefined) else
                        source[field]
                        for key, field in model.items()}
                item['url'] = source.url_path

                self.static_search[source.alt].append(item)

    @check_enabled
    def on_after_build_all(self, builder, **extra):
        for alt, pages in self.static_search.items():
            filename = os.path.join(builder.env.root_path,
                                    self.options['output_path'],
                                    'static_search_{}.json'.format(alt))

            try:
                with open(filename, 'r') as f:
                    contents = f.read()
            except IOError:
                contents = ""

            if contents != json.dumps(pages):
                with open(filename, 'w') as f:
                    f.write(json.dumps(pages))

                reporter.report_generic('generated static search file{}'.format(
                    filename))
