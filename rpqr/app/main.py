import networkx
from rpqr.library.RPQRConfiguration import RPQRConfiguration
from rpqr.loader import RPQRLoader
from rpqr.query.language.interpreter import RPQRInterpreter
from rpqr.query.language.parser import RPQRParser
from rpqr.query.language.scanner import RPQRScanner
import matplotlib.pyplot as plt

if __name__ == "__main__":
    config = RPQRConfiguration(["/home/tkorbar/development/rpqr/rpqr/loader/plugins/implementations"], [("local-repo", "http://download.eng.brq.redhat.com/composes/candidates-rhel-8/RHEL-8/latest-RHEL-8.4.0/compose/AppStream/x86_64/os/")])
    loader = RPQRLoader(config)
    graph = loader.createDatabase()
    scnr = RPQRScanner(config)
    parser = RPQRParser(config)
    tokens = scnr.getTokens("DEPENDSON 'cups-lpd-1:2.2.6-38.el8.x86_64' 1")
    AST = parser.parseTokens(tokens)
    interpreter = RPQRInterpreter(config)
    result = interpreter.performCommands(graph, AST)
    labelDict = {}
    for nodeId in result:
        labelDict[nodeId] = graph.nodes[nodeId]["name"]
    pos = networkx.spring_layout(result)

    networkx.draw(result, pos=pos, with_labels = True, labels=labelDict)
    plt.show()
    print("finish")