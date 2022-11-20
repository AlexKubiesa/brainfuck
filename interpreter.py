
import sys


class Interpreter:
    def __init__(self, debug=False):
        self._memory_size = 30_000
        self._debug = debug
        self.reset()
    
    def reset(self):
        self._memory = [0] * self._memory_size
        self._pointer = 0
        self._program = None
        self._program_index = -1

    def run(self, program):
        self._program = program
        while self._program_index < len(program) - 1:
            self._program_index += 1
            c = program[self._program_index]
            match c:
                case "+":
                    self._increment()
                case "-":
                    self._decrement()
                case ">":
                    self._move_right()
                case "<":
                    self._move_left()
                case ",":
                    self._read_char()
                case ".":
                    self._write_char()
                case "[":
                    self._start_loop()
                case "]":
                    self._end_loop()

    def _increment(self):
        if self._memory[self._pointer] >= 255:
            self._memory[self._pointer] = 0
        else:
            self._memory[self._pointer] += 1
        if self._debug:
            print(f"Incremented cell {self._pointer}. New value: {self._memory[self._pointer]}.")
    
    def _decrement(self):
        if self._memory[self._pointer] <= 0:
            self._memory[self._pointer] = 255
        else:
            self._memory[self._pointer] -= 1
        if self._debug:
            print(f"Decremented cell {self._pointer}. New value: {self._memory[self._pointer]}.")
    
    def _move_right(self):
        if self._pointer >= self._memory_size - 1:
            raise Exception("Memory bounds exceeded.")
        else:
            self._pointer += 1
        if self._debug:
            print(f"Moved pointer right to cell {self._pointer}.")
    
    def _move_left(self):
        if self._pointer <= 0:
            raise Exception("Memory bounds exceeded.")
        else:
            self._pointer -= 1
        if self._debug:
            print(f"Moved pointer left to cell {self._pointer}.")
    
    def _read_char(self):
        c = sys.stdin.read(1)
        val = ord(c)
        if val > 255:
            raise Exception("Invalid ASCII character.")
        self._memory[self._pointer] = val
        if self._debug:
            print(f"Read character code {val}.")

    def _write_char(self):
        val = self._memory[self._pointer]
        c = chr(val)
        sys.stdout.write(c)
        if self._debug:
            print(f"Wrote character code {val}.")
    
    def _start_loop(self):
        if self._memory[self._pointer] == 0:
            closing_index = self._find_closing_bracket_index(self._program, self._program_index)
            self._program_index = closing_index
            if self._debug:
                print(f"Skipped loop. jumped to cell {self._pointer}.")
    
    def _end_loop(self):
        if self._memory[self._pointer] != 0:
            opening_index = self._find_opening_bracket_index(self._program, self._program_index)
            self._program_index = opening_index
            if self._debug:
                print(f"Repeated loop. jumped to cell {self._pointer}.")
    
    @staticmethod
    def _find_closing_bracket_index(program, opening_bracket_index):
        level = 0
        for i in range(opening_bracket_index + 1, len(program)):
            match program[i]:
                case "[":
                    level += 1
                case "]":
                    if level > 0:
                        level -= 1
                    else:
                        return i
        raise Exception(f"Opening bracket at index {opening_bracket_index} has no matching closing bracket.")
    
    @staticmethod
    def _find_opening_bracket_index(program, closing_bracket_index):
        level = 0
        for i in reversed(range(0, closing_bracket_index)):
            match program[i]:
                case "[":
                    if level > 0:
                        level -= 1
                    else:
                        return i
                case "]":
                    level += 1
        raise Exception(f"Closing bracket at index {closing_bracket_index} has no matching opening bracket.")


if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename) as f:
        program = f.read()
    interpreter = Interpreter()
    interpreter.run(program)
    
