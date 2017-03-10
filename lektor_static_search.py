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
    description = (u'Serialize sources contents to json'
                   'for using with static search js libraries.')

    def __init__(self, *args, **kwargs):
        """Initialice class atributes and define options default values."""
        Plugin.__init__(self, *args, **kwargs)
        self.static_search = defaultdict(list)
        self.enabled = False
        self.models = defaultdict(dict)
        self.options = {'output_path': 'static-search', }

    def check_enabled(func):
        """Function decorator to deactivate functions if plugin isn't enabled."""

        def func_wrapper(self, *args, **kwargs):
            if not self.enabled:
                return
            func(self, *args, **kwargs)

        return func_wrapper

    def on_server_spawn(self, **extra):
        """Check if plugin is active (i.e. static-search flag is present)."""
        extra_flags = extra.get("extra_flags") \
            or extra.get("build_flags") or {}
        self.enabled = bool(extra_flags.get('static-search'))

    def on_setup_env(self, **extra):
        """Load config options into self.models and self.options dicts."""
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
        """Delete previous contents of self.static_search dict, and create output folder."""
        self.static_search.clear()

        output_path = os.path.join(builder.env.root_path,
                                   self.options['output_path'])
        if not os.path.exists(output_path):
            os.makedirs(output_path)

    @check_enabled
    def on_before_build(self, source, prog, **extra):
        """Extract information from Sources and save it in self.staic_search dict."""
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
        """Dump each alternative entry of the self.staic_search dict to json and save it."""
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

                reporter.report_generic(
                    'generated static search file{}'.format(filename))
