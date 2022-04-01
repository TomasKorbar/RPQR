'''
Project: RPQR
Author: Tomáš Korbař (tomas.korb@seznam.cz)
Copyright 2021 - 2022 Tomáš Korbař
'''

import logging
import os
import sys
import importlib
from typing import List, Tuple

from rpqr.loader.plugins.library import RPQRBasePlugin
from rpqr.query.commands import RPQRFilteringCommand


class RPQRConfiguration:
    """
    Configuration class meant for loading plugins and setting
    up query language configuration (types of terminal and non-terminal symbols).
    """

    def __init__(self, pluginDirectories: List[str], repositories: List[Tuple[str, str]], userConfiguration: dict = {}) -> None:
        """Initialize instance of RPQRConfiguration

        :param pluginDirectories: Directories containing plugin modules.
        :type pluginDirectories: List[str]
        :param repositories: list of tuples containing repository alias and URL.
        :type repositories: List[Tuple[str, str]]
        """
        self.pluginDirectories = pluginDirectories
        self.userConfiguration = dict(userConfiguration)
        logging.basicConfig(level=logging.INFO)
        self.rootLogger = logging.getLogger("RPQR")
        self._logger = self.rootLogger.getChild("RPQRConfiguration")
        self.plugins = list()
        self._initializePlugins()
        self.repositories = repositories
        # terminal symbols for our language
        self.tokenTypes = {"leftBracelet": 0, "rightBracelet": 1, "and": 3, "or": 4,
                           "number": 5, "string": 6, "command": 7, "end": 8, "loadMore": 9, "collapse": 10, "not": 11, "comma": 12}
        # terminals starting commands
        self.commandTypes = {}
        # special characters allowed in string literals
        self.allowedSpecialCharacters = ['&', '|', '-', '.', ':', '_', '~', '+', '^']
        # since we need to use additional non terminals in parser,
        # we will make the index public to avoid any collision
        # with existing symbols
        self.commandIndex = len(self.tokenTypes)+1
        for plugin in self.plugins:
            plugin: RPQRBasePlugin
            for command in plugin.implementedCommands:
                command: RPQRFilteringCommand
                self.commandTypes[command.name] = self.commandIndex
                self.commandIndex += 1

    def _initializePlugins(self):
        """ Load plugins from supplied directories
        """
        for dir in self.pluginDirectories:
            sys.path.append(dir)
            pluginModules = os.listdir(dir)
            for file in pluginModules:
                moduleName = file[:-3]
                # if file name starts with _ then it is most likely not a plugin
                if moduleName.startswith("_"):
                    continue
                cfg = None
                if moduleName in self.userConfiguration.keys():
                    cfg = self.userConfiguration[moduleName]

                if (cfg != None and cfg.get("disabled") == "1"):
                    self._logger.info(
                        "%s plugin was disabled in configuration" % moduleName)
                    continue
                module = importlib.import_module(moduleName)
                pluginClass = getattr(module, moduleName)

                pluginInstance = pluginClass(rootLogger=self.rootLogger,
                                            config=cfg)
                self.plugins.append(pluginInstance)

    def isAttributeSupported(self, attributes: List[str]) -> Tuple[bool, str]:
        """ Find out whether attributes are supported by this configuration

        :param attributes: attributes which should be checked
        :type attributes: List[str]
        :return: Tuple with boolean indicating whether attributes are supported and
                 string with first unsupported attribute when needed.
        :rtype: Tuple[bool, str]
        """
        for attr in attributes:
            currCheck = False
            for plugin in self.plugins:
                if plugin.desiredName == attr:
                    currCheck = True
                    break
            if not currCheck:
                return (False, attr)
        return (True, "")
