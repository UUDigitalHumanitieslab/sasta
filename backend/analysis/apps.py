# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class AnalysisConfig(AppConfig):
    name = 'analysis'

    def ready(self):
        import analysis.signals  # noqa: F401
