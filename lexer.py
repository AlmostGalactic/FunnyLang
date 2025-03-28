def find_col(line, start, predicate):
    while start < len(line) and not predicate(line[start]):
        start += 1
    return start

def strip_col(line, col):
    while col < len(line) and line[col].isspace():
        col += 1
    return col

def chop_word(line, col):
    while col < len(line) and not line[col].isspace():
        col += 1
    return col

def lex_line(line):
    col = 0
    length = len(line)

    def peek(offset=0):
        return line[col + offset] if col + offset < length else ''

    while col < length:
        # Skip whitespace
        while col < length and line[col].isspace():
            col += 1

        if col >= length:
            break

        # Handle comment
        if peek() == '/' and peek(1) == '/':
            break  # Ignore the rest of the line

        # Handle quoted strings
        if peek() in ('"', "'"):
            quote = peek()
            start_col = col
            col += 1
            string_value = ''
            while col < length:
                if peek() == '\\' and col + 1 < length:
                    esc = peek(1)
                    if esc == 'n':
                        string_value += '\n'
                    elif esc == 't':
                        string_value += '\t'
                    elif esc == '\\':
                        string_value += '\\'
                    elif esc == quote:
                        string_value += quote
                    else:
                        string_value += esc  # unrecognized escape
                    col += 2
                elif peek() == quote:
                    col += 1
                    break
                else:
                    string_value += line[col]
                    col += 1
            yield (start_col, quote + string_value + quote)
            continue


        # Handle regular tokens
        start_col = col
        while col < length and not line[col].isspace() and not (peek() == '/' and peek(1) == '/') and line[col] not in ('"', "'"):
            col += 1
        yield (start_col, line[start_col:col])




def lex_file(file_path):
    with open(file_path, "r") as f:
        return [(file_path, row, col, token)
                for (row, line) in enumerate(f.readlines())
                for (col, token) in lex_line(line)]
        
if __name__ == "__main__":
    line = 'name = "John // not a comment" // actual comment'
    print(list(lex_line(line)))
