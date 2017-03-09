# -*- coding: utf-8 -*-
from lektor.pluginsystem import Plugin


class TipueSearchPlugin(Plugin):
    name = u'Lektor Tipue Search'
    description = u'Add your description here.'

    def on_process_template_context(self, context, **extra):
        def test_function():
            return 'Value from plugin %s' % self.name
        context['test_function'] = test_function
