from rpqr.loader import RPQRLoader
from rpqr.query.scanner.RPQRScanner import RPQRScanner

if __name__ == "__main__":
    scnr = RPQRScanner(["/home/tkorbar/development/rpqr/rpqr/loader/plugins/implementations"])
    tokens = scnr.getTokens("NAME 'hello'")
    print("finish")