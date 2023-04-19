import graphviz as gv


class FlowCreator:

	__enableMode = False
	__enableName = []

	@staticmethod
	def disableAll():
		FlowCreator.__enableMode = True
		FlowCreator.__enableName = []

	@staticmethod
	def enableAll():
		FlowCreator.__enableMode = False

	@staticmethod
	def enableOne(name: str):
		if FlowCreator.__enableMode:
			FlowCreator.__enableName.append(name)

	def __init__(self, font: str = "SimHei", useLr: bool = False):
		self.graph = gv.Digraph()
		if useLr:
			self.graph.graph_attr = {"rankdir": "LR"}
		self.graph.node_attr = {"shape": "box", "fontname": font}
		self.graph.edge_attr = {"fontname": font}
		self.next_id = 1
		self.need_neato = False

	def createNode(self,
	               label: str,
	               pos: tuple[int] = None,
	               shape=None,
	               style=None) -> int:
		args = {}
		if pos != None:
			args["pos"] = "%f,%f!" % (pos[0], pos[1])
			self.need_neato = True
		if shape != None:
			args["shape"] = shape
		if style != None:
			args["style"] = style
		self.graph.node(str(self.next_id), str(label), args)
		self.next_id += 1
		return self.next_id - 1

	def createEdge(self,
	               from_id: int,
	               to_id: int | list[int],
	               label: str = "",
	               style=None):
		if isinstance(to_id, list):
			for i in to_id:
				self.createEdge(from_id, i, label=label, style=style)
		else:
			args = {}
			if style != None:
				args["style"] = style
			self.graph.edge(str(from_id), str(to_id), label, args)

	def render(self,
	           name: str = "graph",
	           format: str = "png",
	           engine: str | None = None):
		if FlowCreator.__enableMode and not name in FlowCreator.__enableName:
			return
		if engine == None:
			if self.need_neato:
				engine = "neato"
			else:
				engine = "dot"
		self.graph.render(name, directory="result", format=format, engine=engine)

	# def createSubGraph(self, nodes):
	# 	pass
