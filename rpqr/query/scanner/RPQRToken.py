class RPQRToken:
    def __init__(self, type : int = None, content : str = ""):
        self.type = type
        self.content = content

    def appendToContent(self, what : str):
        self.content += what