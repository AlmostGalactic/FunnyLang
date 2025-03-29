from lexer import *
from keywords import *

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

def run_program(stack=[], program=[], func={}, get_funcs=False, vars={}, return_vars=False, scope=False, parent_scope=None, is_if_block=False):
    ip = 0
    functions = func.copy()
    
    # Create proper scope chain
    # For if statements, use the parent scope directly (no new scope)
    if is_if_block:
        local_vars = parent_scope
        parent = None
    # For other blocks with scope, create a new local scope dictionary
    elif scope:
        local_vars = {}
        parent = parent_scope if parent_scope is not None else vars
    else:
        # Global scope
        local_vars = vars
        parent = None
    
    # Track variables that are declared in this scope (not needed for if blocks)
    scope_declarations = set() if not is_if_block else None

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
                # Pass the current scope directly - no new scope for if blocks
                run_program(stack, true_block, functions, vars=vars, is_if_block=True, parent_scope=local_vars)
            elif else_ip != 0:
                false_block = get_block_code(program, else_ip + 1, end_ip)
                # Pass the current scope directly - no new scope for if blocks
                run_program(stack, false_block, functions, vars=vars, is_if_block=True, parent_scope=local_vars)
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
            attachment_funcs = run_program(stack, attachment_program, functions, get_funcs=True)
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
            while True:
                if not stack:
                    break
                condition = float(stack[-1])
                if condition == 0:
                    ip = while_end_ip
                    break
                # Create a new scope for while loops
                run_program(stack, while_program, functions, vars=vars, scope=True, parent_scope=local_vars)

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
            # Add variable to local scope
            local_vars[var_name] = 0
            # Track declaration only if we're tracking (not in if blocks)
            if scope_declarations is not None:
                scope_declarations.add(var_name)

        elif op[0] == SET_VAR and not get_funcs:
            var_name = stack.pop()
            var_value = stack.pop()
            
            # If we're in an if block or this is a global var
            if is_if_block or not scope:
                local_vars[var_name] = var_value
            # If variable was declared in this scope, update it
            elif var_name in local_vars:
                local_vars[var_name] = var_value
            # If we're in a scoped block and it's a parent variable
            elif parent is not None and var_name in parent:
                parent[var_name] = var_value
            else:
                # Variable doesn't exist anywhere in scope chain, create locally
                local_vars[var_name] = var_value
                if scope_declarations is not None:
                    scope_declarations.add(var_name)

        elif op[0] == WORD and not get_funcs:
            word = op[1]
            if word in functions:
                # Execute function
                run_program(stack, functions[word], functions, vars=vars, scope=True, parent_scope=local_vars)
            # First check local vars
            elif word in local_vars:
                stack.append(local_vars[word])
            # Then check parent scope (only if in a nested scope)
            elif not is_if_block and scope and parent is not None and word in parent:
                stack.append(parent[word])
            else:
                raise Exception(f"Unknown word: {word}")
        
        ip += 1

    # Return both functions and variables if requested
    return (functions, vars) if return_vars else functions

def simulate_program(program):
    stack = []
    functions = {}
    functions, variables = run_program(stack, program, functions, get_funcs=True, return_vars=True)
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