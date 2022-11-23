import sys
import itertools


class Tokens:
    Left = "<"
    Right = ">"
    StartLoop = "["
    EndLoop = "]"
    Increment = "+"
    Decrement = "-"
    Read = ","
    Write = "."
    All = [
        Left,
        Right,
        StartLoop,
        EndLoop,
        Increment,
        Decrement,
        Read,
        Write
    ]

    @classmethod
    def is_comment(cls, token):
        return token not in cls.All


class Lexer:
    def __init__(self, program):
        self._program = program
    
    def get_tokens(self):
        return [token for token in self._program if not Tokens.is_comment(token)]


class Node:
    def __init__(self, children):
        self._children = children

    @property
    def children(self):
        return self._children


class TokenNode(Node):
    def __init__(self, token):
        super().__init__([])
        self._token = token

    @property
    def token(self):
        return self._token


class SequenceNode(Node):
    def __init__(self, children):
        super().__init__(children)


class LoopNode(Node):
    def __init__(self, start, body, end):
        super().__init__([start, body, end])
        self._start = start
        self._body = body
        self._end = end

    @property
    def start(self):
        return self._start

    @property
    def body(self):
        return self._body

    @property
    def end(self):
        return self._end


class AddSubtractNode(Node):
    def __init__(self, value):
        super().__init__([])
        self._value = value
    
    @property
    def value(self):
        return self._value


class MovePointerNode(Node):
    def __init__(self, displacement):
        super().__init__([])
        self._displacement = displacement
    
    @property
    def displacement(self):
        return self._displacement


class SetZeroNode(Node):
    def __init__(self):
        super().__init__([])


class SetValueNode(Node):
    def __init__(self, value):
        super().__init__([])
        self._value = value
    
    @property
    def value(self):
        return self._value


class MoveMemoryNode(Node):
    def __init__(self, displacement, multiplier=1):
        super().__init__([])
        self._displacement = displacement
        self._multiplier = multiplier
    
    @property
    def displacement(self):
        return self._displacement

    @property
    def multiplier(self):
        return self._multiplier


class Parser:
    def __init__(self, lexer):
        self._lexer = lexer

    def parse(self):
        tokens = self._lexer.get_tokens()
        return self._parse_sequence(tokens)

    def _parse_sequence(self, tokens):
        children = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            match token:
                case Tokens.Left | Tokens.Right | Tokens.Increment | Tokens.Decrement | Tokens.Read | Tokens.Write:
                    children.append(self._parse_leaf(token))
                case Tokens.StartLoop:
                    end_loop_index = self._find_end_loop_index(tokens, i)
                    loop = tokens[i:end_loop_index+1]
                    children.append(self._parse_loop(loop))
                    i = end_loop_index
                case _:
                    raise Exception(f"Unexpected character '{token}'.")
            i += 1
        return SequenceNode(children)
    
    def _parse_leaf(self, token):
        return TokenNode(token)

    def _find_end_loop_index(self, tokens, start_loop_index):
        i = start_loop_index
        level = 0
        while i < len(tokens):
            match tokens[i]:
                case Tokens.StartLoop:
                    level += 1
                case Tokens.EndLoop:
                    level -= 1
                    if level == 0:
                        return i
            i += 1
        raise Exception(f"Loop was not closed. Tokens: {tokens}, Loop start index: {start_loop_index}, Nesting level: {level}.")
    
    def _parse_loop(self, tokens):
        start = self._parse_leaf(tokens[0])
        body = self._parse_sequence(tokens[1:-1])
        end = self._parse_leaf(tokens[-1])
        return LoopNode(start, body, end)


class ParseTreeRewriter:
    def rewrite(self, tree):
        if isinstance(tree, TokenNode):
            return self.rewrite_token_node(tree)
        elif isinstance(tree, SequenceNode):
            return self.rewrite_sequence_node(tree)
        elif isinstance(tree, LoopNode):
            return self.rewrite_loop_node(tree)
        elif isinstance(tree, AddSubtractNode):
            return self.rewrite_add_subtract_node(tree)
        elif isinstance(tree, MovePointerNode):
            return self.rewrite_move_pointer_node(tree)
        elif isinstance(tree, SetZeroNode):
            return self.rewrite_set_zero_node(tree)
        elif isinstance(tree, SetValueNode):
            return self.rewrite_set_value_node(tree)
        elif isinstance(tree, MoveMemoryNode):
            return self.rewrite_move_memory_node(tree)
        else:
            raise Exception(f"Unexpected node type {type(tree)}.")
    
    def rewrite_token_node(self, node):
        return node

    def rewrite_sequence_node(self, node):
        return SequenceNode([self.rewrite(child) for child in node.children])

    def rewrite_loop_node(self, node):
        return LoopNode(self.rewrite(node.start), self.rewrite(node.body), self.rewrite(node.end))

    def rewrite_add_subtract_node(self, node):
        return node
    
    def rewrite_move_pointer_node(self, node):
        return node

    def rewrite_set_zero_node(self, node):
        return node
    
    def rewrite_set_value_node(self, node):
        return node
    
    def rewrite_move_memory_node(self, node):
        return node
    

class IncrementDecrementCombiningTreeRewriter(ParseTreeRewriter):
    def rewrite_sequence_node(self, node):
        children = []
        i = 0
        while i < len(node.children):
            if isinstance(node.children[i], TokenNode) and (node.children[i].token in [Tokens.Increment, Tokens.Decrement]):
                value = 1 if (node.children[i].token == Tokens.Increment) else -1
                j = i + 1
                while j < len(node.children) and isinstance(node.children[j], TokenNode) and (node.children[j].token in [Tokens.Increment, Tokens.Decrement]):
                    value += 1 if (node.children[j].token == Tokens.Increment) else -1
                    j += 1
                children.append(AddSubtractNode(value))
                i = j
            else:
                children.append(self.rewrite(node.children[i]))
                i += 1
        return SequenceNode(children)


class LeftRightCombiningTreeRewriter(ParseTreeRewriter):
    def rewrite_sequence_node(self, node):
        children = []
        i = 0
        while i < len(node.children):
            if isinstance(node.children[i], TokenNode) and (node.children[i].token in [Tokens.Left, Tokens.Right]):
                displacement = 1 if (node.children[i].token == Tokens.Right) else -1
                j = i + 1
                while j < len(node.children) and isinstance(node.children[j], TokenNode) and (node.children[j].token in [Tokens.Left, Tokens.Right]):
                    displacement += 1 if (node.children[j].token == Tokens.Right) else -1
                    j += 1
                children.append(MovePointerNode(displacement))
                i = j
            else:
                children.append(self.rewrite(node.children[i]))
                i += 1
        return SequenceNode(children)
    
    def rewrite_loop_node(self, node):
        return LoopNode(node.start, self.rewrite(node.body), node.end)


class SetZeroRecognisingTreeRewriter(ParseTreeRewriter):
    def rewrite_loop_node(self, node):
        body = self.rewrite(node.body)
        if (len(body.children) == 1) and (body.children[0].token == Tokens.Decrement):
            return SetZeroNode()
        else:
            return LoopNode(node.start, body, node.end)


class SetValueRecognisingTreeRewriter(ParseTreeRewriter):
    def rewrite_sequence_node(self, node):
        children = []
        i = 0
        while i < len(node.children):
            if isinstance(node.children[i], SetZeroNode):
                value = 0
                j = i + 1
                while j < len(node.children):
                    if isinstance(node.children[j], SetZeroNode):
                        value = 0
                    elif isinstance(node.children[j], AddSubtractNode):
                        value += node.children[j].value
                    else:
                        break
                    j += 1
                children.append(SetValueNode(value))
                i = j
            else:
                children.append(self.rewrite(node.children[i]))
                i += 1
        return SequenceNode(children)


class MoveMemoryRecognisingTreeRewriter(ParseTreeRewriter):
    def rewrite_loop_node(self, node):
        body = self.rewrite(node.body)
        move_memory = self.recognise_move_memory(body.children)
        if move_memory:
            displacement, multiplier = move_memory
            return MoveMemoryNode(displacement, multiplier)
        else:
            return LoopNode(node.start, body, node.end)
    
    def recognise_move_memory(self, nodes):
        if len(nodes) != 4:
            return None

        if isinstance(nodes[0], AddSubtractNode):
            subtract_node = nodes[0]
            add_node = nodes[2]
            move_nodes = nodes[1], nodes[3]
        elif isinstance(nodes[3], AddSubtractNode):
            subtract_node = nodes[3]
            add_node = nodes[1]
            move_nodes = nodes[0], nodes[2]
        else:
            return None

        if subtract_node.value != -1:
            return None

        if not isinstance(add_node, AddSubtractNode):
            return None

        if not all(map(lambda x: isinstance(x, MovePointerNode), move_nodes)):
            return None

        displacement = move_nodes[0].displacement
        if displacement == 0:
            return None

        if move_nodes[1].displacement != -displacement:
            return None
        
        multiplier = add_node.value
        return displacement, multiplier


class Compiler:
    def __init__(self, parser, emitter):
        self._parser = parser
        self._emitter = emitter

    def compile(self):
        self._generate_header()
        tree = self._parser.parse()
        tree = SetZeroRecognisingTreeRewriter().rewrite(tree)
        tree = IncrementDecrementCombiningTreeRewriter().rewrite(tree)
        tree = SetValueRecognisingTreeRewriter().rewrite(tree)
        tree = LeftRightCombiningTreeRewriter().rewrite(tree)
        tree = MoveMemoryRecognisingTreeRewriter().rewrite(tree)
        self._generate_body(tree)
    
    def _generate_header(self):
        self._emitter.emit_header()
        self._emitter.emit_blank_line()
    
    def _generate_body(self, tree):
        if isinstance(tree, TokenNode):
            match tree.token:
                case Tokens.Left:
                    self._emitter.emit_left()
                case Tokens.Right:
                    self._emitter.emit_right()
                case Tokens.Increment:
                    self._emitter.emit_add()
                case Tokens.Decrement:
                    self._emitter.emit_subtract()
                case Tokens.Read:
                    self._emitter.emit_read()
                case Tokens.Write:
                    self._emitter.emit_write()
                case _:
                    raise Exception(f"Unexpected token '{tree.token}'.")
        elif isinstance(tree, SequenceNode):
            for child in tree.children:
                self._generate_body(child)
        elif isinstance(tree, LoopNode):
            self._emitter.begin_loop()
            self._generate_body(tree.body)
            self._emitter.end_loop()
            self._emitter.emit_blank_line()
        elif isinstance(tree, AddSubtractNode):
            if tree.value > 0:
                self._emitter.emit_add(tree.value)
            elif tree.value < 0:
                self._emitter.emit_subtract(-tree.value)
        elif isinstance(tree, MovePointerNode):
            if tree.displacement > 0:
                self._emitter.emit_right(tree.displacement)
            elif tree.displacement < 0:
                self._emitter.emit_left(-tree.displacement)
        elif isinstance(tree, SetZeroNode):
            self._emitter.emit_set_value(0)
        elif isinstance(tree, SetValueNode):
            self._emitter.emit_set_value(tree.value)
        elif isinstance(tree, MoveMemoryNode):
            self._emitter.emit_move_memory(tree.displacement, tree.multiplier)
        else:
            raise Exception(f"Unexpected node type {type(tree)}.")


class CodeEmitter:
    def __init__(self, outfile):
        self._outfile = outfile
        self._indent_level = 0
    
    def _write_line(self, line):
        indent = " " * 4 * self._indent_level
        self._outfile.write(indent + line + "\n")
    
    def emit_header(self):
        self._write_line("import sys")
        self._write_line("memory = [0] * 30_000")
        self._write_line("pointer = 0")

    def emit_left(self, amount=1):
        self._write_line(f"pointer -= {amount}")
    
    def emit_right(self, amount=1):
        self._write_line(f"pointer += {amount}")

    def emit_read(self):
        self._write_line("memory[pointer] = ord(sys.stdin.read(1))")
    
    def emit_write(self):
        self._write_line("sys.stdout.write(chr(memory[pointer]))")
    
    def begin_loop(self):
        self._write_line("while memory[pointer]:")
        self._indent_level += 1
    
    def end_loop(self):
        self._indent_level -= 1
    
    def emit_blank_line(self):
        self._write_line("")
    
    def emit_add(self, value=1):
        self._write_line(f"memory[pointer] += {value}")
    
    def emit_subtract(self, value=1):
        self._write_line(f"memory[pointer] -= {value}")
    
    def emit_set_value(self, value):
        self._write_line(f"memory[pointer] = {value}")
    
    def emit_move_memory(self, displacement, multiplier):
        if displacement == 0:
            raise ValueError("Displacement cannot be zero.")
        if multiplier == 0:
            return
            
        pointer_suffix = f" + {displacement}" if (displacement > 0) else (f" - {-displacement}")
        assignment = "+=" if (multiplier > 0) else "-="
        abs_multiplier = abs(multiplier)

        self._write_line(f"memory[pointer{pointer_suffix}] {assignment} {abs_multiplier} * memory[pointer]")
        self._write_line("memory[pointer] = 0")


if __name__ == "__main__":
    inpath = sys.argv[1]
    outpath = sys.argv[2]

    with open(inpath) as infile:
        program = infile.read()

    lexer = Lexer(program)
    parser = Parser(lexer)
    with open(outpath, "w") as outfile:
        emitter = CodeEmitter(outfile)
        compiler = Compiler(parser, emitter)
        compiler.compile()
