import os
import sys
import importlib
from rpqr.loader.plugins.library import RPQRBasePlugin
from rpqr.query.commands import RPQRFilteringCommand

class RPQRConfiguration:
    def __init__(self, pluginDirectories, repositories):
        self.pluginDirectories = pluginDirectories
        self.plugins = list()
        self._initializePlugins()
        self.repositories = repositories

        self.tokenTypes = {"leftBracelet": 0, "rightBracelet": 1, "and": 3, "or": 4,
                "number": 5, "string": 6, "command": 7, "end": 8, "loadMore": 9, "collapse": 10}
        self.commandTypes = {}
        self.allowedSpecialCharacters = ['&', '|', '-', '.']
        self.commandIndex = 11
        for plugin in self.plugins:
            plugin: RPQRBasePlugin
            for command in plugin.implementedCommands:
                command: RPQRFilteringCommand
                self.commandTypes[command.name] = self.commandIndex
                self.commandIndex += 1

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
