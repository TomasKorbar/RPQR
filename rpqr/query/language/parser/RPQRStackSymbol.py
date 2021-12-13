class RPQRStackSymbol:
    def __init__(self, type, children: list = [], operator: str = None):
        self.children = children
        self.operator = operator
        self.type = type
