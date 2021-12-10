from typing import Optional
from urllib.parse import ParseResult, urlparse
import logging
import xml.etree.ElementTree as XMLTreeModule
import bz2
import gzip
import zipfile
from tempfile import NamedTemporaryFile
import requests


class Loader:
    XMLNamespaces = {"repo": "http://linux.duke.edu/metadata/repo"}

    def __init__(self, repositories: list):
        self.repositories = repositories

    def createDatabase(self) -> bool:
        packageList = []
        for repo in self.repositories:
            try:
                parsedUrl = urlparse(repo)
            except ValueError as e:
                logging.error("Invalid repository url was supplied %s" % (e))
                return False
            dbFileData: str = self._getPrimaryDatabaseFile(parsedUrl)
            if dbFileData is None:
                return False

    def _getPrimaryDatabaseFile(self, url: ParseResult) -> Optional[str]:
        dbFile = None
        if url.scheme == "file":
            dbFile = self._getLocalPrimaryDatabaseFile(url)
        elif url.scheme == "http" or url.scheme == "https":
            dbFile = self._getRemotePrimaryDatabaseFile(url)
        else:
            logging.error(
                "provided repository url uses unsupported scheme %s" % (url.scheme))
            return False

        return dbFile

    def _getRemotePrimaryDatabaseFile(self, url: ParseResult) -> Optional[str]:
        repomdData = None
        locationObject: XMLTreeModule.Element = None
        compressedData = None
        try:
            repomdData = requests.get(
                url.geturl() + "/repodata/repomd.xml")
        except requests.exceptions.RequestException as e:
            logging.error(
                "Was unable to download repomd of repository at %s" % (url.geturl()))
            return None

        xmlObject: XMLTreeModule.ElementTree = XMLTreeModule.fromstring(
            repomdData.text)
        try:
            locationObject = xmlObject.findall(
                './repo:data[@type="primary"]/repo:location[@href]', self.XMLNamespaces)[0]
        except IndexError as e:
            logging.error(
                "Repository at %s has corrupted repomd file" % (url.geturl()))
            return None

        try:
            compressedData = requests.get(url.geturl() +
                                          ("/%s" % (locationObject.attrib["href"])))
        except requests.exceptions.RequestException as e:
            logging.error(
                "Was unable to download primary database of repository at %s" % (url.geturl()))
            return None

        return self._decompressDatabaseFile(data=compressedData.content)

    def _getLocalPrimaryDatabaseFile(self, url: ParseResult) -> Optional[str]:
        repomdPath = url.path + "/repodata/repomd.xml"
        xmlObject: XMLTreeModule.ElementTree = None
        locationObject: XMLTreeModule.Element = None
        try:
            xmlObject = XMLTreeModule.parse(repomdPath)
        except XMLTreeModule.ParseError as e:
            logging.error(
                "Could not access repomd file of repository at %s" % (url.path))
            return None

        try:
            locationObject = xmlObject.findall(
                './repo:data[@type="primary"]/repo:location[@href]', self.XMLNamespaces)[0]
        except IndexError as e:
            logging.error(
                "Repository at %s has corrupted repomd file" % (url.path))
            return None

        return self._decompressDatabaseFile(url.path + ("/%s" % (locationObject.attrib["href"])))

    def _decompressDatabaseFile(self, path: str = None, data: bytes = None) -> Optional[str]:
        decompressedData = str()
        if path is not None:
            try:
                with open(path, "rb") as compressedFile:
                    decompressedData = self._decompressBytes(
                        compressedFile.read())
            except OSError as e:
                logging.error(
                    "Was unable to open compressed primary database file of repository at %s" % (path))
                return None
        else:
            decompressedData = self._decompressBytes(data)

        return decompressedData

    def _decompressBytes(self, data: bytes) -> Optional[str]:
        try:
            if data[0:3] == b"\x1f\x8b\x08":
                return str(gzip.decompress(data))
            elif data[0:3] == b"\x42\x5a\x68":
                return str(bz2.decompress(data))
            else:
                logging.error("Primary database in unknown format")
                return None
        except OSError as e:
            logging.error("Was unable to decompress primary database")
            return None


if __name__ == "__main__":
    loader = Loader(
        ["file:///var/tmp/junk/repo"])
    loader.createDatabase()
