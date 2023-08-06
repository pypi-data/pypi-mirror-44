from django.apps import AppConfig
from . import monkeypatch


class TemplateSupersuperConfig(AppConfig):
    name = 'template_supersuper'

    def ready(self):
        monkeypatch.doit()

