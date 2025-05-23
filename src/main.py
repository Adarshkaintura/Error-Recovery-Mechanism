from flask import Flask, request, render_template
import subprocess
import os

app = Flask(
    __name__,
    template_folder='C:\\Users\\rajsh\\Downloads\\ERMP\\templates',
    static_folder='C:\\Users\\rajsh\\Downloads\\ERMP\\static'
)

symbol_table = {}

def generate_token_stream(code):
    try:
        project_root = 'C:\\Users\\rajsh\\Downloads\\ERMP'
        result = subprocess.run(
            ["bin\\lexer.exe"],
            input=code,
            capture_output=True,
            text=True,
            shell=True,
            cwd=project_root
        )
        if result.returncode != 0:
            error = f"Lexer error: {result.stderr}"
            print(error)
            return error
        output = result.stdout or "No lexer output"
        print(f"Lexer output: {output}")
        # Simulate token stream dynamically
        tokens = []
        parts = code.replace(";", " ; ").replace("=", " = ").replace("+", " + ").replace(">", " > ").replace("*", " * ").replace("-", " - ").replace("(", " ( ").replace(")", " ) ").split()
        for part in parts:
            if part == "int":
                tokens.append("INT")
            elif part == ";":
                tokens.append("SEMICOLON")
            elif part == "=":
                tokens.append("EQUALS")
            elif part == "+":
                tokens.append("PLUS")
            elif part == ">":
                tokens.append("GREATER")
            elif part == "*":
                tokens.append("TIMES")
            elif part == "-":
                tokens.append("MINUS")
            elif part == "(":
                tokens.append("LPAREN")
            elif part == ")":
                tokens.append("RPAREN")
            elif part == "if":
                tokens.append("IF")
            elif part.isdigit():
                tokens.append(f"NUMBER({part})")
            elif part.strip():
                tokens.append(f"IDENTIFIER({part})")
        simulated_tokens = " ".join(tokens)
        print(f"Simulated tokens: {simulated_tokens}")
        return simulated_tokens
    except Exception as e:
        error = f"Lexer failed: {str(e)}"
        print(error)
        return error

def generate_parse_tree(code):
    try:
        project_root = 'C:\\Users\\rajsh\\Downloads\\ERMP'
        result = subprocess.run(
            ["bin\\parser.exe"],
            input=code,
            capture_output=True,
            text=True,
            shell=True,
            cwd=project_root
        )
        if result.returncode != 0:
            error = f"Parser error: {result.stderr}"
            print(error)
            return error
        output = result.stdout or "No parser output"
        print(f"Parser output: {output}")
        # Simulate a parse tree structure
        simulated_tree = "Program\n"
        lines = code.split(";")
        for line in lines:
            line = line.strip()
            if line:
                if "int" in line:
                    var = line.split()[1]
                    simulated_tree += f"  Declaration -> Type INT IDENTIFIER({var})\n"
                elif "=" in line:
                    var = line.split("=")[0].strip()
                    expr = line.split("=")[1].strip()
                    simulated_tree += f"  Assignment -> IDENTIFIER({var}) = Expression({expr})\n"
        print(f"Simulated parse tree: {simulated_tree}")
        return simulated_tree
    except Exception as e:
        error = f"Parser failed: {str(e)}"
        print(error)
        return error

def semantic_analysis(code):
    global symbol_table
    symbol_table.clear()  # Reset symbol table
    errors = []
    lines = code.split("\n")
    # Populate symbol table with declared variables
    for line in lines:
        if "int" in line and ";" in line:
            var = line.replace("int", "").replace(";", "").strip()
            symbol_table[var] = "int"
    # Check for undeclared variables
    for line in lines:
        if "=" in line:
            var = line.split("=")[0].strip()
            if var not in symbol_table:
                errors.append(f"Undeclared variable: {var}. Suggestion: Declare as 'int {var};'")
    print(f"Symbol table: {symbol_table}")
    print(f"Semantic errors: {errors}")
    return errors

def generate_intermediate_code(code):
    intermediate = []
    lines = code.split(";")
    temp_count = 1
    for line in lines:
        line = line.strip()
        if "=" in line:
            var = line.split("=")[0].strip()
            expr = line.split("=")[1].strip()
            if "+" in expr:
                op1, op2 = expr.split("+")
                op1, op2 = op1.strip(), op2.strip()
                intermediate.append(f"t{temp_count} = {op1} + {op2}")
                intermediate.append(f"{var} = t{temp_count}")
                temp_count += 1
            else:
                intermediate.append(f"{var} = {expr}")
    output = "\n".join(intermediate) if intermediate else "No intermediate code"
    print(f"Intermediate code: {output}")
    return output

def create_graphviz_tree(parse_output):
    try:
        from graphviz import Digraph
        dot = Digraph()
        lines = parse_output.split("\n")
        for i, line in enumerate(lines):
            if line.strip():
                dot.node(str(i), line)
                if i > 0:
                    dot.edge(str(i-1), str(i))
        static_path = 'C:\\Users\\rajsh\\Downloads\\ERMP\\static\\parse_tree'
        dot.render(static_path, format="png", cleanup=True)
        print(f"Graphviz generated: {static_path}.png")
        return "parse_tree.png"
    except Exception as e:
        error = f"Graphviz error: {str(e)}"
        print(error)
        return error

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        code = request.form["code"]
        print(f"Received code: {code}")
        token_stream = generate_token_stream(code)
        parse_output = generate_parse_tree(code)
        semantic_errors = semantic_analysis(code)
        intermediate_code = generate_intermediate_code(code)
        tree_image = create_graphviz_tree(parse_output)
        print(f"Rendering with tree_image: {tree_image}")
        return render_template(
            "index.html",
            code=code,
            tokens=token_stream,
            parse_tree=parse_output,
            semantic_errors=semantic_errors,
            intermediate_code=intermediate_code,
            tree_image=tree_image
        )
    return render_template("index.html", code="")

if __name__ == "__main__":
    app.run(debug=True, port=5000)