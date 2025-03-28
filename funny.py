from lexer import *
from keywords import *

def isNum(x):
    return str(x).replace('.', '', 1).isdigit()

def isStr(x):
    return str(x).startswith('"') and x.endswith('"')

def parse_token_as_op(token):
    (file_path, row, col, word) = token

    if word == "+":
        return plus()
    elif word == "-":
        return sub()
    elif word == "*":
        return mul()
    elif word == "/":
        return div()
    elif word == "%":
        return mod()
    elif word == ".":
        return dump()
    elif word == "dup":
        return dup()
    elif word == "if":
        return iff()
    elif word == "end":
        return end()
    elif word == "=":
        return equal()
    elif word == "@":
        return set_var()
    elif word == "<":
        return lt()
    elif word == ">":
        return gt()
    elif word == "write":
        return write()
    elif word == "while":
        return whil()
    elif word == "input":
        return inp()
    elif word == "func":
        return func()
    elif word == "not":
        return no()
    elif word == "attach":
        return attach()
    elif word == "pop":
        return popp()
    elif word == ":":
        return roll()
    elif word == "else":
        return elsee()
    elif word == "var":
        return var()
    else:
        if isNum(word):
            return push(word)
        elif isStr(word):
            if word.startswith(("\"")) and word.endswith(("\"")):
                word = word[1:-1]
            return push(word)
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
    code = []
    ip = start
    while ip < end:
        op = program[ip]
        code.append(op)
        ip += 1
    return code

def run_program(stack=[], program=[], func={}, get_funcs=False, vars = {}, return_vars=False):
    ip = 0
    functions = func.copy()
    variables = vars
    while ip < len(program):
        op = program[ip]
        if op[0] == PLUS and (not get_funcs):
            a = float(stack.pop())
            b = float(stack.pop())
            stack.append(float(b+a))
        elif op[0] == PUSH:
            stack.append(op[1])
        elif op[0] == SUB and (not get_funcs):
            a = float(stack.pop())
            b = float(stack.pop())
            stack.append(float(b-a))
        elif op[0] == MUL and (not get_funcs):
            a = float(stack.pop())
            b = float(stack.pop())
            stack.append(float(b*a))
        elif op[0] == DIV and (not get_funcs):
            a = float(stack.pop())
            b = float(stack.pop())
            stack.append(float(b/a))
        elif op[0] == MOD and (not get_funcs):
            a = float(stack.pop())
            b = float(stack.pop())
            stack.append(float(b%a))
        elif op[0] == DUMP and (not get_funcs):
            a = stack.pop()
            print(float(a), end="")
        elif op[0] == WRITE and (not get_funcs):
            a = stack.pop()
            print(str(a), end="")
        elif op[0] == DUP and (not get_funcs):
            a = stack.pop()
            stack.append(float(a))
            stack.append(float(a))
        elif op[0] == INPUT and (not get_funcs):
            a = input("\n? ")
            stack.append(a)
        elif op[0] == IF and (not get_funcs):
            condition = float(stack.pop())
            else_ip, end_ip = codeblock(program, ip, useElse=True)
            if condition:
                true_end = else_ip if else_ip != 0 else end_ip
                true_block = get_block_code(program, ip + 1, true_end)
                run_program(stack, true_block, functions)
            elif else_ip != 0:
                false_block = get_block_code(program, else_ip + 1, end_ip)
                run_program(stack, false_block, functions)
            ip = end_ip
        elif op[0] == NOT and (not get_funcs):
            a = float(stack.pop())
            stack.append(0 if a > 0 else 1)
        elif op[0] == END and (not get_funcs):
            pass
        elif op[0] == EQUAL and (not get_funcs):
            a = stack.pop()
            b = stack.pop()
            if isNum(a) and isNum(b):
                result = float(b) == float(a)
            else:
                result = str(b) == str(a)
            stack.append(float(result))
        elif op[0] == GT and (not get_funcs):
            a = stack.pop()
            b = stack.pop()
            if isNum(a) and isNum(b):
                result = float(b) > float(a)
            else:
                result = str(b) > str(a)
            stack.append(float(result))
        elif op[0] == LT and (not get_funcs):
            a = stack.pop()
            b = stack.pop()
            if isNum(a) and isNum(b):
                result = float(b) < float(a)
            else:
                result = str(b) < str(a)
            stack.append(float(result))
        elif op[0] == ATTACH:
            attachment = stack.pop()
            attachment_program = load_program_from_file(str(attachment))
            attachment_funcs = run_program(stack, attachment_program, functions, True)
            functions.update(attachment_funcs)
        elif op[0] == POP and (not get_funcs):
            stack.pop()
        elif op[0] == ROLL and (not get_funcs):
            n = 1
            if n < 0 or n >= len(stack):
                raise IndexError(f"ROLL error: index {n} out of bounds for stack of size {len(stack)}")
            val = stack[-(n + 1)]
            del stack[-(n + 1)]
            stack.append(val)
        elif op[0] == WHILE and (not get_funcs):
            while_ip = ip
            while_end_ip = codeblock(program, while_ip)
            while_program = get_block_code(program, while_ip + 1, while_end_ip)
            while True:
                condition = float(stack[-1])
                if condition == 0:
                    ip = while_end_ip
                    break
                run_program(stack, while_program, functions)
                if stack == []:
                    stack.append(condition)
        elif op[0] == FUNC:
            func_name = program[ip+1][1]
            func_code_start = ip + 2
            func_ip_end = codeblock(program, ip)
            func_code = get_block_code(program, func_code_start, func_ip_end)
            functions[func_name] = func_code
            ip = func_ip_end
        elif op[0] == VAR:
            ip += 1
            var_name = program[ip][1]
            variables[var_name] = 0
        elif op[0] == SET_VAR:
            var_name = stack.pop()
            var_value = stack.pop()
            
            if var_name in variables:
                variables[var_name] = var_value
            else:
                assert False, f"Unknown variable name: {var_name}"
        elif not get_funcs:
            if op[1] in functions:
                run_program(stack, functions[op[1]], functions)
            elif op[1] in variables:
                stack.append(variables[op[1]])
            else:
                assert False, f"Unknown word: {op[1]}"
        ip += 1
    if return_vars:
        return functions, variables
    else:
        return functions

def simulate_program(program):
    stack = []
    functions = {}
    functions, variables = run_program(stack, program, functions, True, return_vars=True)
    if "main" in functions:
        run_program(program=functions["main"], func=functions, vars=variables)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python funny.py <program.funny>")
        sys.exit(1)
    filename = sys.argv[1]
    program = load_program_from_file(filename)
    simulate_program(program)
