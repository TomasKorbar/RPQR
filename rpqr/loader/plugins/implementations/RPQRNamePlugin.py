from rpqr.loader.plugins.library import RPQRDataPlugin

class RPQRNamePlugin(RPQRDataPlugin):
    desiredName = "Name"
    desiredType = str
    
    def prepareData(self, pkg):
        return str(pkg)