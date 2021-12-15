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
    #tokens = scnr.getTokens("WHATDEPENDSON 'libyang-1.0.184-2.fc33.x86_64' 2 & ~(NAMELIKE 'frr' | NAMELIKE 'devel')")
    #tokens = scnr.getTokens("MAINTAINER 'mruprich' & DEPENDSONUSER 'tkorbar' 0")
    #tokens = scnr.getTokens("MAINTAINER 'mruprich' & DEPENDSONUSER 'tkorbar' 0")
    # VISUALIZE(MAINTAINER('mruprich') & DEPENDSONUSER('tkorbar',0)) & NAMELIKE('kappa')
    tokens = scnr.getTokens("SUBSETNAMELIKE('cpp', SUBSETNAMELIKE('devel', NAMELIKE('libyang'))) & NAMELIKE('i686')")
    AST = parser.parseTokens(tokens)
    interpreter = RPQRInterpreter(config)
    
    result = interpreter.performCommands(graph, AST)





    labelDict = {}
    for nodeId in result:
        labelDict[nodeId] = graph.nodes[nodeId]["name"]

    networkx.draw_spring(result, with_labels = True, labels=labelDict, )

    plt.show()
    print("finish")