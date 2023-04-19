import graphviz as gv


class UmlCreator:

	__enableMode = False
	__enableName = []

	@staticmethod
	def disableAll():
		UmlCreator.__enableMode = True
		UmlCreator.__enableName = []

	@staticmethod
	def enableAll():
		UmlCreator.__enableMode = False

	@staticmethod
	def enableOne(name):
		if UmlCreator.__enableMode:
			UmlCreator.__enableName.append(name)

	@staticmethod
	def renderSingleClass(name,
	                      bases=None,
	                      props=None,
	                      methods=None,
	                      format="png",
	                      engine="dot"):
		uc = UmlCreator()
		bases = uc.__wrapArg(bases)
		for i in bases:
			uc.addSimplifiedClass(i)
		uc.addClass(name, bases=bases, props=props, methods=methods)
		uc.render(name, format, engine)

	def __init__(self):
		self.graph = gv.Digraph()
		self.graph.graph_attr = {
		    "fontname": "Helvetica,Arial,sans-serif",
		    "labelloc": "t"
		}
		self.graph.edge_attr = {
		    "fontname": "Helvetica,Arial,sans-serif",
		}
		self.graph.node_attr = {
		    "fontname": "Helvetica,Arial,sans-serif",
		    "shape": "record",
		    "style": "filled",
		    "fillcolor": "gray95",
		}
		self.classIds = {}
		self.nextId = 1

	def __wrapArg(self, arg):
		if type(arg) is str:
			return [arg]
		elif isinstance(arg, list):
			return arg
		else:
			return []

	def __processArg(self, s: str):
		s = s.strip()

		if s == "":
			return ""
		if not s[0] in ["+", "#", "-"]:
			s = "+ " + s

		sLen = len(s)

		if s[1] != " ":
			s = s[0] + " " + s[1:]
			sLen += 1

		scIndex = 0
		while True:
			scIndex = s.find(":", scIndex + 1)
			if (scIndex < sLen - 1 and
			    s[scIndex + 1] == ":") or (scIndex > 0 and s[scIndex - 1] == ":"):
				continue
			if scIndex < 0:
				break
			if scIndex > 0 and s[scIndex - 1] != " ":
				s = s[:scIndex] + " " + s[scIndex:]
				sLen += 1
				scIndex += 1
			if scIndex < sLen - 1 and s[scIndex + 1] != " ":
				s = s[:scIndex + 1] + " " + s[scIndex + 1:]
				sLen += 1

		return s

	def addClass(self,
	             name: str,
	             bases: str | list[str] | None = None,
	             props: str | list[str] | None = None,
	             methods: str | list[str] | None = None,
	             composedOf: str | list[str] | None = None):
		(props, methods, bases,
		 composedOf) = map(self.__wrapArg, (props, methods, bases, composedOf))

		label = "{" + name + "|"
		for i in props:
			prop = self.__processArg(i)
			label += prop
			label += "\\l"

		label += "|"

		for i in methods:
			method = self.__processArg(i)
			label += method
			label += "\\l"

		label += "}"
		self.graph.node(str(self.nextId), label)
		self.classIds[name] = str(self.nextId)
		self.nextId += 1
		for i in bases:
			self.addInheritance(i, name)
		for i in composedOf:
			self.addComposition(i, name)

	def addSimplifiedClass(self,
	                       name: str | list[str] | None,
	                       bases: str | list[str] | None = None,
	                       composedOf: str | list[str] | None = None):
		(bases, composedOf) = map(self.__wrapArg, (bases, composedOf))

		label = "{" + name + "}"
		self.graph.node(str(self.nextId), label)
		self.classIds[name] = str(self.nextId)
		self.nextId += 1
		for i in bases:
			self.addInheritance(i, name)
		for i in composedOf:
			self.addComposition(i, name)

	def addInheritance(self, base: str, derive: str):
		self.graph.edge(
		    self.classIds[base],
		    self.classIds[derive],
		    arrowhead="none",
		    arrowtail="onormal",
		    dir="back")

	def addDependency(self, depender: str, depended: str):
		self.graph.edge(
		    self.classIds[depended],
		    self.classIds[depender],
		    arrowhead="none",
		    arrowtail="vee",
		    style="dashed",
		    dir="back")

	def addComposition(self, member: str, compose: str):
		self.graph.edge(
		    self.classIds[member], self.classIds[compose], arrowhead="odiamond")

	def addDirectLine(self, class1: str, class2: str, label: str = "", args={}):
		self.graph.edge(self.classIds[class1], self.classIds[class2], label, args)

	def render(self,
	           name: str = "graph",
	           format: str = "png",
	           engine: str = "dot"):
		if UmlCreator.__enableMode and not name in UmlCreator.__enableName:
			return
		self.graph.render(filename="result/" + name, format=format, engine=engine)
