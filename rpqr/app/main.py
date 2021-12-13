import networkx
from rpqr.loader import RPQRLoader
from rpqr.query.language.interpreter import RPQRInterpreter
from rpqr.query.language.parser import RPQRParser
from rpqr.query.language.scanner import RPQRScanner
import matplotlib.pyplot as plt

if __name__ == "__main__":
    loader = RPQRLoader(["/home/tkorbar/development/rpqr/rpqr/loader/plugins/implementations"], [("local-repo", "http://download.eng.brq.redhat.com/composes/candidates-rhel-8/RHEL-8/latest-RHEL-8.4.0/compose/AppStream/x86_64/os/")])
    graph = loader.createDatabase()
    scnr = RPQRScanner(["/home/tkorbar/development/rpqr/rpqr/loader/plugins/implementations"])
    parser = RPQRParser(["/home/tkorbar/development/rpqr/rpqr/loader/plugins/implementations"])
    tokens = scnr.getTokens("NAMELIKE 'cups' & NAMELIKE 'devel'")
    AST = parser.parseTokens(tokens)
    interpreter = RPQRInterpreter(["/home/tkorbar/development/rpqr/rpqr/loader/plugins/implementations"])
    result = interpreter.performCommands(graph, AST)
    labelDict = {}
    for nodeId in result:
        labelDict[nodeId] = graph.nodes[nodeId]["name"]
    networkx.draw(result, with_labels = True, labels=labelDict)
    plt.show()
    print("finish")