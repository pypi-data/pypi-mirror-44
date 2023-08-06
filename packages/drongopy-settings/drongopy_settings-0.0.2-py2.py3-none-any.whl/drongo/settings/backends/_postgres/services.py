from .models import ModuleSetting, db


class SettingsServiceBase(object):
    @classmethod
    def init(cls, module):
        cls.module = module
        db.initialize(module.database.instance.get())
        models = [
            ModuleSetting
        ]
        for model in models:
            module.database.instance.auto_migrate(model)


class SettingsSet(SettingsServiceBase):
    def __init__(self, mod, settings):
        self.mod = mod
        self.settings = settings

    def call(self, ns='core'):
        settings, _ = ModuleSetting.get_or_create(module=self.mod, _ns=ns)
        settings.settings = self.settings
        settings.save()


class SettingsGet(SettingsServiceBase):
    def __init__(self, mod):
        self.mod = mod

    def call(self, ns='core'):
        return ModuleSetting.get_or_none(module=self.mod, _ns=ns)
