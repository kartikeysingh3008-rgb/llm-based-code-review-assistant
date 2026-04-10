import ast

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.loops = 0
        self.max_depth = 0
        self.current_depth = 0

    def visit_FunctionDef(self, node):
        function_length = len(node.body)

        self.functions.append({
            "name": node.name,
            "length": function_length
        })

        self.generic_visit(node)

    def visit_For(self, node):
        self.loops += 1
        self._track_depth(node)

    def visit_While(self, node):
        self.loops += 1
        self._track_depth(node)

    def visit_If(self, node):
        self._track_depth(node)

    def _track_depth(self, node):
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)
        self.generic_visit(node)
        self.current_depth -= 1


def analyze_code(code):
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return {"error": "Invalid Python code"}

    analyzer = CodeAnalyzer()
    analyzer.visit(tree)

    return {
        "functions": analyzer.functions,
        "loops": analyzer.loops,
        "max_nesting_depth": analyzer.max_depth
    }