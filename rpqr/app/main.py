from rpqr.loader import RPQRLoader
from rpqr.query.parser import RPQRParser
from rpqr.query.scanner import RPQRScanner

if __name__ == "__main__":
    scnr = RPQRScanner(["/home/tkorbar/development/rpqr/rpqr/loader/plugins/implementations"])
    parser = RPQRParser(["/home/tkorbar/development/rpqr/rpqr/loader/plugins/implementations"])
    tokens = scnr.getTokens("NAME 'hello' & NAME 'world'")
    statement = parser.parseTokens(tokens)

    print("finish")