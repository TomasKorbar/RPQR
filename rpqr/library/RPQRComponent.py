import sys
import os
import importlib


class RPQRComponent:
    def __init__(self, pluginDirectories):
        self.pluginDirectories = pluginDirectories
        self.plugins = list()
        self._initializePlugins()

    def _initializePlugins(self):
        for dir in self.pluginDirectories:
            sys.path.append(dir)
            pluginModules = os.listdir(dir)

        for file in pluginModules:
            moduleName = file[:-3]
            if moduleName.startswith("_"):
                continue
            module = importlib.import_module(moduleName)
            pluginClass = getattr(module, moduleName)
            pluginInstance = pluginClass()
            self.plugins.append(pluginInstance)
