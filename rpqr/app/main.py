import networkx
from rpqr.library.RPQRConfiguration import RPQRConfiguration
from rpqr.loader import RPQRLoader
from rpqr.query.language.interpreter import RPQRInterpreter
from rpqr.query.language.parser import RPQRParser
from rpqr.query.language.scanner import RPQRScanner
import matplotlib.pyplot as plt

if __name__ == "__main__":
    config = RPQRConfiguration(["/home/tkorbar/development/rpqr/rpqr/loader/plugins/implementations"],
                               [("fedora-repo", "http://ftp.fi.muni.cz/pub/linux/fedora/linux/releases/33/Everything/x86_64/os/")])
    loader = RPQRLoader(config)
    graph = loader.createDatabase()
    scnr = RPQRScanner(config)
    parser = RPQRParser(config)
    interpreter = RPQRInterpreter(config)
    AST = parser.parseTokens(scnr.getTokens("MAINTAINER('orphan')"))
    result = interpreter.performCommands(graph, AST)
    for node in list(result.nodes):
        AST = parser.parseTokens(scnr.getTokens("WHATDEPENDSON('%s', 20)" % graph.nodes[node]["name"]))
        dependentPackages = interpreter.performCommands(graph, AST)
        maintainerList = []
        for pkgId in list(dependentPackages.nodes):
            for maintainer in dependentPackages.nodes[pkgId]["maintainer"]:
                if maintainer not in maintainerList:
                    maintainerList.append(maintainer)
        maintainerList.remove('orphan')
        print("%s => " % graph.nodes[node]["name"], end="")
        for maint in maintainerList:
            print("%s " % maint, end="")
        print()




    """

    labelDict = {}
    for nodeId in result:
        labelDict[nodeId] = graph.nodes[nodeId]["name"]

    networkx.draw_spring(result, with_labels = True, labels=labelDict, )

    plt.show()
    """
    print("finish")