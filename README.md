# FunnyLang

> **Note**: This language is heavily inspired by [Porth](https://gitlab.com/tsoding/porth) by Tsoding.

FunnyLang is a simple, stack-based, interpreted language implemented in Python. It uses postfix (Reverse Polish) notation for operations and supports variables, conditionals, loops, and function definitions. This repository contains:

- **funny.py** - The main interpreter.
- **lexer.py** - A simple tokenizer/lexer.
- **keywords.py** - An enumeration of token types and helper functions.
- **funny.bat** - Windows batch script to run `.funny` files easily.
- **Libraries/std.funny** - A standard library containing useful functions.

---

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Project Structure](#project-structure)
4. [Installation & Requirements](#installation--requirements)
5. [How to Run FunnyLang](#how-to-run-funnylang)
6. [Language Basics](#language-basics)
    - [Stack-Based Execution](#stack-based-execution)
    - [Operators](#operators)
    - [Variables](#variables)
    - [Functions](#functions)
    - [Conditionals](#conditionals)
    - [Loops](#loops)
    - [Attachments (Imports)](#attachments-imports)
7. [Standard Library (std.funny)](#standard-library-stdfunny)
8. [Example Program](#example-program)
9. [License](#license)

---

## Overview

FunnyLang is a **postfix**, **stack-oriented** language. Instead of writing `a + b`, you push `a` and `b` onto the stack, then apply the operator `+`. You can define functions, variables, and control flow structures such as `if`, `else`, `while`, etc. The language is intended to be minimalistic yet expressive enough for small scripting tasks.

---

## Features
- **Stack-based operations**: Push operands onto the stack and then apply operations.
- **Control flow**: `if ... end`, `else`, and `while ... end` constructs.
- **Functions**: Define named functions with `func <name> ... end`.
- **Variables**: Declare variables with `var <name>` and assign with `@`.
- **Standard library**: Common operations like `print`, `true`, `false`, basic arithmetic definitions, etc.

---

## Project Structure
```
.
├── funny.py        	# Main interpreter
├── lexer.py        	# Tokenizes .funny files
├── keywords.py     	# Enumeration of keywords and helper functions
├── funny.bat       	# Batch script for Windows to run .funny files
└── Libraries
    └── std.funny   	# Standard library of helpful functions
    └── useless.funny   # Useless functions that you might never need
```

---

## Installation & Requirements
- Python 3.x

No external libraries are required beyond standard Python. Just clone or download this repository, and you can run `funny.py` directly.

---

## How to Run FunnyLang

You can run a FunnyLang program in two ways:

1. **Directly with Python**:
   ```bash
   python funny.py path/to/program.funny
   ```
2. **Using the provided batch file (Windows)**:
   ```bash
   funny.bat path\to\program.funny
   ```
   This will pause after execution so you can see the output.

---

## Language Basics

### Stack-Based Execution
FunnyLang works with a stack. Every time you write a literal (number or string), it is **pushed** onto the stack. Operators then act on the top elements of the stack.

- **PUSH**: Numbers and quoted strings (e.g., `5`, `"Hello"`) are automatically pushed.
- **Arithmetic** (`+`, `-`, `*`, `/`, `%`): Pops the top two items from the stack, applies the operation, and pushes the result back.
- **dump (.)**: Pops the top of the stack and prints it as a **number** without a newline.
- **write**: Pops the top of the stack and prints it as **string/text** without a newline.
- **dup**: Duplicates the top element of the stack.

### Operators
Below are some key operators you’ll see in the code:

| Operator/Keyword | Description                                                       |
|------------------|-------------------------------------------------------------------|
| `+`              | Add the top two numbers on the stack.                             |
| `-`              | Subtract the top of the stack from the second top.                |
| `*`              | Multiply the top two numbers.                                     |
| `/`              | Divide the second top by the top.                                 |
| `%`              | Modulo (second top mod top).                                      |
| `.` (dot)        | Print the top of the stack (as a number), no newline.             |
| `write`          | Print the top of the stack as text, no newline.                   |
| `dup`            | Duplicate the top of the stack.                                   |
| `pop`            | Pop the top element from the stack.                               |
| `:` (roll)       | Takes the top element and rotates it under the next element (stack manipulation). |
| `attach`         | Attach/import another `.funny` file.                              |
| `input`          | Prompt user input and push it onto the stack.                     |

### Variables
Variables are declared with `var <name>`:
```
var myVar
```
This defines `myVar` in the current environment with a default value of `0`.

To **get** the value of a variable, just write its name:
```
myVar
```
It pushes the current value of `myVar` onto the stack.

To **set** a variable, push the new value first, then push the variable name, and finally use `@`:
```
42
"myVar"
@
```
This sets `myVar` to 42.

### Functions
Define a function with:
```
func <functionName>
    ... function body ...
end
```
Call it simply by writing its name:
```
<functionName>
```
That will execute all instructions in the function body.

### Conditionals
FunnyLang provides `if`, `else`, and `end` for conditionals. The structure is:
```
<condition> if
    ... code if true ...
else
    ... code if false ...
end
```
- The `<condition>` is expected to be a number on the stack (non-zero is true, zero is false).
- The `else` part is optional.

Example:
```
5 10 > if
   "5 is greater than 10" write
else
   "5 is not greater than 10" write
end
```

### Loops
Use `while` and `end` for loops. The pattern is:
```
<condition> while
    ... code ...
end
```
The loop will keep running as long as the condition on the top of the stack is non-zero. Typically, you update that condition inside the loop.

Example:
```
var counter

10 "counter" @     // set counter to 10

1 while 	   // 1 is just there to get the while loop started, it will get remove in the loop and replaced with the condition
    pop            // pop the condition check so it doesn't clutter the stack
    counter      // push current value of counter
    1 -            // subtract 1
    "counter" @    // set new value to counter

    "Looping!\n" write

    counter 0 >
end
```

### Attachments (Imports)
Use `attach` to include another `.funny` file:
```
"./Libraries/std.funny" attach
```
This merges the functions from `std.funny` into the current environment. You can then call those functions directly.

---

## Standard Library (std.funny)
Within `./Libraries/std.funny`, you'll find a collection of basic helper functions:

- **print** – Prints the top of tbhe stack along with a newline.
- **false** – Pushes `0`.
- **true** – Pushes `1`.
- **add / sub / mult / div** – Aliases for `+`, `-`, `*`, `/`.
- **roll** – Alias for `:`.
- **square** – Squares the top of the stack.
- **double** – Doubles the top of the stack.
- **odd** – Tests if top of stack is odd (pushes `1` or `0`).
- **even** – Tests if top of stack is even (pushes `1` or `0`).
- **set** – Alias for `@` (set variable).
- **pow** – Raises a number to a given exponent (handles negative exponents as well).

These functions serve as building blocks for more complex FunnyLang programs.

---

## Example Program

Create a file called `example.funny` with the following content:

```bash
// example.funny
"./Libraries/std.funny" attach    // load standard library

func main
    5 6 add               	  // 5 + 6
    print                     	  // print result
    "Hello, FunnyLang!" print
end
```

Then run:
```bash
python funny.py example.funny
```
or on Windows:
```bash
funny.bat example.funny
```

You should see:
```
11
Hello, FunnyLang!
```
