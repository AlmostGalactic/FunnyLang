from lexer import *
from keywords import *

class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def define(self, name, value=0):
        # Called when we see `var <name>`
        self.vars[name] = value

    def get(self, name):
        # Look up variable in this env or parent
        if name in self.vars:
            return self.vars[name]
        if self.parent is not None:
            return self.parent.get(name)
        raise Exception(f"Unknown variable: {name}")

    def set(self, name, value):
        # Search for existing var in chain of environments
        if name in self.vars:
            self.vars[name] = value
        elif self.parent is not None:
            self.parent.set(name, value)
        else:
            # If not found in parents, create new variable in current scope
            self.vars[name] = value

def isNum(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

def isStr(x):
    return str(x).startswith('"') and x.endswith('"')

def parse_token_as_op(token):
    (file_path, row, col, word) = token

    if word == "+": return plus()
    elif word == "-": return sub()
    elif word == "*": return mul()
    elif word == "/": return div()
    elif word == "%": return mod()
    elif word == ".": return dump()
    elif word == "dup": return dup()
    elif word == "if": return iff()
    elif word == "end": return end()
    elif word == "=": return equal()
    elif word == "@": return set_var()
    elif word == "<": return lt()
    elif word == ">": return gt()
    elif word == "write": return write()
    elif word == "while": return whil()
    elif word == "input": return inp()
    elif word == "func": return func()
    elif word == "not": return no()
    elif word == "attach": return attach()
    elif word == "pop": return popp()
    elif word == ":": return roll()
    elif word == "else": return elsee()
    elif word == "var": return var()
    else:
        if isNum(word):
            return push(word)
        elif isStr(word):
            return push(word[1:-1])
        else:
            return wordd(word)

def load_program_from_file(file_path):
    return [parse_token_as_op(token) for token in lex_file(file_path)]

def codeblock(program, start, useElse=False):
    depth = 0
    else_ip = 0
    end_ip = 0
    ip = start
    while ip < len(program):
        op = program[ip]
        op_type = op[0]
        if op_type in [IF, WHILE, FUNC]:
            depth += 1
        elif op_type == END:
            depth -= 1
            if depth == 0:
                end_ip = ip
                break
        elif useElse and op_type == ELSE and depth == 1:
            else_ip = ip
        ip += 1
    if end_ip < 1:
        raise Exception("Missing 'end' for code block")
    return (else_ip, end_ip) if useElse else end_ip

def get_block_code(program, start, end):
    return program[start:end]

def run_program(stack=None, program=None, func=None,
                get_funcs=False, env=None, return_vars=False,
                is_if_block=False):
    if stack is None:
        stack = []
    if program is None:
        program = []
    if func is None:
        func = {}
    if env is None:
        # Global environment if not provided
        env = Environment()

    ip = 0
    functions = func.copy()

    while ip < len(program):
        op = program[ip]

        if op[0] == PLUS and not get_funcs:
            a = float(stack.pop())
            b = float(stack.pop())
            stack.append(float(b + a))

        elif op[0] == PUSH:
            stack.append(op[1])

        elif op[0] == SUB and not get_funcs:
            a = float(stack.pop())
            b = float(stack.pop())
            stack.append(float(b - a))

        elif op[0] == MUL and not get_funcs:
            a = float(stack.pop())
            b = float(stack.pop())
            stack.append(float(b * a))

        elif op[0] == DIV and not get_funcs:
            a = float(stack.pop())
            b = float(stack.pop())
            stack.append(float(b / a))

        elif op[0] == MOD and not get_funcs:
            a = float(stack.pop())
            b = float(stack.pop())
            stack.append(float(b % a))

        elif op[0] == DUMP and not get_funcs:
            print(float(stack.pop()), end="")

        elif op[0] == WRITE and not get_funcs:
            print(str(stack.pop()), end="")

        elif op[0] == DUP and not get_funcs:
            a = float(stack[-1])
            stack.append(a)

        elif op[0] == INPUT and not get_funcs:
            a = input("\n? ")
            stack.append(a)

        elif op[0] == IF and not get_funcs:
            condition = float(stack.pop())
            else_ip, end_ip = codeblock(program, ip, useElse=True)
            if condition:
                true_end = else_ip if else_ip != 0 else end_ip
                true_block = get_block_code(program, ip + 1, true_end)

                # CHANGED HERE: We reuse 'env' instead of creating if_env
                run_program(stack, true_block, functions, env=env)
            elif else_ip != 0:
                false_block = get_block_code(program, else_ip + 1, end_ip)
                
                # CHANGED HERE: We reuse 'env'
                run_program(stack, false_block, functions, env=env)

            ip = end_ip

        elif op[0] == NOT and not get_funcs:
            a = float(stack.pop())
            stack.append(0 if a > 0 else 1)

        elif op[0] == END and not get_funcs:
            pass

        elif op[0] == EQUAL and not get_funcs:
            a = stack.pop()
            b = stack.pop()
            result = float(b) == float(a) if isNum(a) and isNum(b) else str(b) == str(a)
            stack.append(float(result))

        elif op[0] == GT and not get_funcs:
            a = stack.pop()
            b = stack.pop()
            result = float(b) > float(a) if isNum(a) and isNum(b) else str(b) > str(a)
            stack.append(float(result))

        elif op[0] == LT and not get_funcs:
            a = stack.pop()
            b = stack.pop()
            result = float(b) < float(a) if isNum(a) and isNum(b) else str(b) < str(a)
            stack.append(float(result))

        elif op[0] == ATTACH:
            attachment = stack.pop()
            attachment_program = load_program_from_file(str(attachment))
            attachment_funcs = run_program(stack, attachment_program, functions,
                                           get_funcs=True, env=env)
            functions.update(attachment_funcs)

        elif op[0] == POP and not get_funcs:
            stack.pop()

        elif op[0] == ROLL and not get_funcs:
            n = 1
            if n < 0 or n >= len(stack):
                raise IndexError(f"ROLL error: index {n} out of bounds for stack of size {len(stack)}")
            val = stack[-(n + 1)]
            del stack[-(n + 1)]
            stack.append(val)

        elif op[0] == WHILE and not get_funcs:
            while_ip = ip
            while_end_ip = codeblock(program, while_ip)
            while_program = get_block_code(program, while_ip + 1, while_end_ip)

            # Create new environment for the while block
            while_env = Environment(parent=env)
            while True:
                if not stack:
                    break
                condition = float(stack[-1])
                if condition == 0:
                    ip = while_end_ip
                    break
                run_program(stack, while_program, functions, env=while_env)
            # after the while loop, we jump here

        elif op[0] == FUNC:
            func_name = program[ip + 1][1]
            func_code_start = ip + 2
            func_ip_end = codeblock(program, ip)
            func_code = get_block_code(program, func_code_start, func_ip_end)
            functions[func_name] = func_code
            ip = func_ip_end

        elif op[0] == VAR:
            ip += 1
            var_name = program[ip][1]
            env.define(var_name, 0)

        elif op[0] == SET_VAR and not get_funcs:
            var_name = stack.pop()
            var_value = stack.pop()
            env.set(var_name, var_value)

        elif op[0] == WORD and not get_funcs:
            word = op[1]
            if word in functions:
                # create environment for function execution
                func_env = Environment(parent=env)
                run_program(stack, functions[word], functions, env=func_env)
            else:
                # treat as variable
                val = env.get(word)
                stack.append(val)
        ip += 1

    if return_vars:
        # return the entire environment's dictionary plus function references
        return (functions, env.vars)
    else:
        return functions

def simulate_program(program):
    stack = []
    functions = {}
    global_env = Environment()
    functions, variables = run_program(stack=stack, program=program,
                                       func=functions, get_funcs=True,
                                       env=global_env, return_vars=True)
    if "main" in functions:
        run_program(program=functions["main"], func=functions, env=global_env)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python funny.py <program.funny>")
        sys.exit(1)
    filename = sys.argv[1]
    program = load_program_from_file(filename)
    simulate_program(program)
