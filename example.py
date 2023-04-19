from flowGen import FlowCreator
from umlGen import UmlCreator

fc = FlowCreator()

# If you want to create new line in your text, use \\n instead of \n
import_node = fc.createNode("from flowGen import FlowCreator")
create_node = fc.createNode("fc = FlowCreator()")
node_node = fc.createNode("node = fc.createNode(\"text\")")
edge_node = fc.createNode("fc.createEdge(node1, node2)")
render_node = fc.createNode("fc.render(name=\"name\")")

fc.createEdge(import_node, create_node)
fc.createEdge(create_node, node_node)
fc.createEdge(node_node, edge_node)
fc.createEdge(edge_node, render_node)

fc.render("UseFlow")

fc2 = FlowCreator()

# If you want to create new line in your text, use \\n instead of \n
dl_node = fc2.createNode(
    "Download graphviz package\\nfrom its official website\\nhttps://graphviz.org/"
)
pip_node = fc2.createNode("pip install graphviz")
enjoy_node = fc2.createNode("Enjoy this library!")

parent_node = fc2.createNode("Complex graph could be drawn using this library.")
hd_node = fc2.createNode("Use a different font instead of SimHei to have a better resolution.")
hd_eg_node = fc2.createNode("fc = FlowCreator(font=\"Helvetica,Arial,sans-serif\")")
svg_node = fc2.createNode("Or use SVG as render format.")
svg_eg_node = fc2.createNode("fc.render(format=\"svg\")")


fc2.createEdge(dl_node, pip_node)
fc2.createEdge(pip_node, enjoy_node)
fc2.createEdge(parent_node, [hd_node, svg_node])
fc2.createEdge(hd_node, hd_eg_node)
fc2.createEdge(svg_node, svg_eg_node)

fc2.render("InstallGraphvizFirst")

uc = UmlCreator()

uc.addSimplifiedClass("object")
uc.addClass(
    "UmlCreator",
    bases="object",
    props=["graph:graphviz.Digraph"],
    methods=[
        "addClass(name:str)", "addSimplifiedClass(name:str)",
        "addDirectLine(class1: str, class2: str, label: str)"
    ])
uc.render("UmlAPIs")
