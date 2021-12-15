class RPQRStackSymbol:
    def __init__(self, type, children: list = [], operator: str = None):
        self.children = children
        self.operator = operator
        self.type = type

    def addChild(self, item):
        self.children.append(item)

    def setChildren(self, children):
        self.children = children
