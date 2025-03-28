iota_counter = 0

def iota(reset=False):
    global iota_counter
    if reset:
        iota_counter = 0
    result = iota_counter
    iota_counter += 1
    return result

DUMP = iota()
PUSH = iota()
PLUS = iota()
SUB = iota()
MUL = iota()
DIV = iota()
DUP = iota()
END = iota()
IF = iota()
EQUAL = iota()
GT = iota()
LT = iota()
WRITE = iota()
FUNC = iota()
WHILE = iota()
INPUT = iota()
WORD = iota()
NOT = iota()
ATTACH = iota()
POP = iota()
ROLL = iota()
MOD = iota()
ELSE = iota()

def write():
    return (WRITE,)
def dup():
    return (DUP,)
def dump():
    return (DUMP,)
def push(x):
    return (PUSH, x)
def plus():
    return (PLUS,)
def sub():
    return (SUB,)
def mul():
    return (MUL,)
def div():
    return (DIV,)
def iff():
    return (IF,)
def end():
    return (END,)
def gt():
    return (GT,)
def lt():
    return (LT,)
def equal():
    return (EQUAL,)
def whil():
    return (WHILE,)
def inp():
    return (INPUT,)
def wordd(x):
    return (WORD, x)
def func():
    return (FUNC,)
def no():
    return (NOT,)
def attach():
    return (ATTACH,)
def popp():
    return (POP,)
def roll():
    return (ROLL,)
def mod():
    return (MOD,)
def elsee():
    return (ELSE,)