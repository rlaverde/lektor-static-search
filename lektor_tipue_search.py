# -*- coding: utf-8 -*-
import os
import json
from collections import defaultdict

from lektor.pluginsystem import Plugin
from lektor.db import Page


class TipueSearchPlugin(Plugin):
    name = u'Lektor Tipue Search'
    description = u'Serialize models contents for using tipue search.'

    def on_setup_env(self, **extra):
        #TODO load configurations

        self.tipue_search = defaultdict(list)

        self.output_path = 'tipue_search'

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def on_before_build_all(self, builder, **extra):
        self.tipue_search.clear()

    def on_before_build(self, source, prog, **extra):
        if isinstance(source, Page):
            #FIXME at the moment only support blog-post
            if source.datamodel.id == 'blog-post':
                item = {'title': source['title'],
                        'text': source['summary'],
                        'tags': source['tags'], }

                self.tipue_search[source.alt].append(item)

    def on_after_build_all(self, builder, **extra):
        for alt, pages in self.tipue_search.items():
            filename = os.path.join(builder.env.root_path, self.output_path,
                                    'tipue_search_{}.json'.format(alt))

            with open(filename, 'r') as f:
                contents = f.read()

            if contents != json.dumps(pages):
                with open(filename, 'w') as f:
                    f.write(json.dumps(pages))
