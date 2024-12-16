def generar_codigo(node, archivo_salida="codigo_p.txt"):
    """Genera el código P a partir de un AST y lo guarda en un archivo."""
    codigo = []  # Lista para almacenar instrucciones con comentarios
    instrucciones = []  # Lista para almacenar solo las instrucciones sin comentarios
    etiquetas = {"contador": 0}  # Contador de etiquetas

    def nueva_etiqueta():
        etiquetas["contador"] += 1
        return f"L{etiquetas['contador']}"

    def procesar_nodo(node):
        if node:
            #print(f"Processing node: {node.type}, leaf: {node.leaf}")
            tipo = node.type

            ### Handle Concrete Nodes (Generate Code) ###

            # Assignments (sent_assign)
            if tipo == "assign" or tipo == "sent_assign":
                var_name = node.children[0].leaf  # Identifier being assigned to
                procesar_nodo(node.children[1])  # Process the assigned expression
                codigo.append(f"sta {var_name}  \t\t # Store value in {var_name}")
                instrucciones.append(f"sta {var_name}")

            # Expressions (expr)
            elif tipo == "expr":
                procesar_nodo(node.children[0])  # Left operand
                if len(node.children) > 1:
                    oper = node.children[1].leaf  # Operator
                    procesar_nodo(node.children[2])  # Right operand
                    operacion = {
                        "+": "adi",
                        "-": "sbi",
                        "*": "mpi",
                        "/": "dvi",
                    }.get(oper, None)
                    if operacion:
                        codigo.append(f"{operacion} \t\t # Operación {oper}")
                        instrucciones.append(operacion)

            # Terms in expressions (term)
            elif tipo == "term":
                # Process the left operand
                procesar_nodo(node.children[0])
                
                # If there is an operator and a right operand, process them
                if len(node.children) > 1:
                    oper = node.children[1].leaf  # Operator (* or /)
                    procesar_nodo(node.children[2])  # Process the right operand
                    operacion = {
                        "*": "mpi",  # Multiplication
                        "/": "dvi",  # Division
                    }.get(oper, None)
                    if operacion:
                        codigo.append(f"{operacion} \t\t # Operación {oper}")
                        instrucciones.append(operacion)

            # Variable Declarations (decl)
            elif tipo == "decl":
                # Process the type and variable list, but no code is generated.
                #procesar_nodo(node.children[0])  # Type (e.g., int, float)
                procesar_nodo(node.children[1])  # List of variables (e.g., x, y)
                # No intermediate code is generated for declarations.

            # Read Statements (sent_read)
            elif tipo == "sent_read":
                var_name = node.children[0].leaf  # Identifier (variable to read into)
                codigo.append(f"lda {var_name} \t\t # Load address of {var_name}")
                instrucciones.append(f"lda {var_name}")
                codigo.append(f"rdi {var_name} \t\t # Read input into {var_name}")
                instrucciones.append(f"rdi {var_name}")

            # Write Statements (sent_write)
            elif tipo == "sent_write":
                procesar_nodo(node.children[0])  # Process the value/expression to write
                codigo.append(f"wri \t\t # Write value to output")
                instrucciones.append("wri")

            # If Statements (sent_if)
            elif tipo == "sent_if":
                etiqueta_salida = nueva_etiqueta()
                procesar_nodo(node.children[0])  # Process condition (exp_bool)
                codigo.append(f"fjp {etiqueta_salida} \t\t # Jump if false")
                instrucciones.append(f"fjp {etiqueta_salida}")
                procesar_nodo(node.children[1])  # Process then-block (bloque)
                if len(node.children) > 2:
                    etiqueta_else = nueva_etiqueta()
                    codigo.append(f"ujp {etiqueta_else} \t\t # Jump to end of else")
                    instrucciones.append(f"ujp {etiqueta_else}")
                    codigo.append(f"lab {etiqueta_salida} \t\t # Else block label")
                    instrucciones.append(f"lab {etiqueta_salida}")
                    procesar_nodo(node.children[2])  # Process else-block
                    codigo.append(f"lab {etiqueta_else} \t\t # End of if-else")
                    instrucciones.append(f"lab {etiqueta_else}")
                else:
                    codigo.append(f"lab {etiqueta_salida} \t\t # End of if")
                    instrucciones.append(f"lab {etiqueta_salida}")

            # While Loops (sent_while)
            elif tipo == "sent_while":
                etiqueta_inicio = nueva_etiqueta()
                etiqueta_salida = nueva_etiqueta()
                codigo.append(f"lab {etiqueta_inicio} \t\t # Start of while loop")
                instrucciones.append(f"lab {etiqueta_inicio}")
                procesar_nodo(node.children[0])  # Process condition (exp_bool)
                codigo.append(f"fjp {etiqueta_salida} \t\t # Jump if false")
                instrucciones.append(f"fjp {etiqueta_salida}")
                procesar_nodo(node.children[1])  # Process loop body (bloque)
                codigo.append(f"ujp {etiqueta_inicio} \t\t # Jump back to start of while")
                instrucciones.append(f"ujp {etiqueta_inicio}")
                codigo.append(f"lab {etiqueta_salida} \t\t # End of while loop")
                instrucciones.append(f"lab {etiqueta_salida}")

            # Do-While Loops (sent_do)
            elif tipo == "sent_do":
                etiqueta_inicio = nueva_etiqueta()
                codigo.append(f"lab {etiqueta_inicio} \t\t # Start of do-while loop")
                instrucciones.append(f"lab {etiqueta_inicio}")
                procesar_nodo(node.children[0])  # Process loop body (bloque)
                procesar_nodo(node.children[1])  # Process condition (exp_bool)
                codigo.append(f"fjp {etiqueta_inicio} \t\t # Jump back to start if true")
                instrucciones.append(f"fjp {etiqueta_inicio}")

            # Boolean Expressions (exp_bool)
            elif tipo == "exp_bool":
                procesar_nodo(node.children[0])  # Left operand
                if len(node.children) > 1:
                    oper = node.children[1].leaf  # Operator (AND, OR)
                    procesar_nodo(node.children[2])  # Right operand
                    operacion = {
                        "AND": "and",
                        "OR": "or",
                    }.get(oper, None)
                    if operacion:
                        codigo.append(f"{operacion} \t\t # Boolean {oper}")
                        instrucciones.append(operacion)

            # Comparisons (igualdad)
            elif tipo == "igualdad":
                procesar_nodo(node.children[0])  # Left operand
                oper = node.children[1].leaf  # Operator (==, !=)
                procesar_nodo(node.children[2])  # Right operand
                operacion = {
                    "==": "equ",
                    "!=": "neq",
                }[oper]
                codigo.append(f"{operacion} \t\t # Comparison {oper}")
                instrucciones.append(operacion)

            # Unary Operations (unario)
            elif tipo == "unario":
                procesar_nodo(node.children[1])  # Operand
                oper = node.children[0].leaf  # Operator (+, -)
                operacion = {
                    "+": None,  # No action needed for unary +
                    "-": "neg",  # Negate the value
                }.get(oper, None)
                if operacion:
                    codigo.append(f"{operacion} \t\t # Unary {oper}")
                    instrucciones.append(operacion)
            
            elif tipo == "rel": 
                procesar_nodo(node.children[0]) # Left operand 
                procesar_nodo(node.children[2]) # Right operand 
                oper = node.children[1].leaf # Relational operator 
                operacion = { "<": "les", "<=": "leq", ">": "grt", ">=": "geq", "==": "equ", "!=": "neq", }[oper] 
                codigo.append(f"{operacion} \t\t # Operación {oper}") 
                instrucciones.append(operacion)

            # Handle exp_value (constants, identifiers, and boolean literals)
            elif tipo == "exp_value":
                print("exp_value found")
                # If the leaf is a number (int/float), load the constant
                if isinstance(node.leaf, (int, float)):
                    codigo.append(f"ldc {node.leaf} \t\t # Load constant {node.leaf}")
                    instrucciones.append(f"ldc {node.leaf}")
                
                # If the leaf is a string (identifier), load the variable's value
                elif isinstance(node.leaf, str):
                    # Check for boolean literals (TRUE, FALSE)
                    if node.leaf.upper() == "TRUE":
                        codigo.append(f"ldc 1 \t\t # Load boolean TRUE (1)")
                        instrucciones.append("ldc 1")
                    elif node.leaf.upper() == "FALSE":
                        codigo.append(f"ldc 0 \t\t # Load boolean FALSE (0)")
                        instrucciones.append("ldc 0")
                    else:
                        # Otherwise, assume it's an identifier
                        codigo.append(f"lod {node.leaf} \t\t # Load value of {node.leaf}")
                        instrucciones.append(f"lod {node.leaf}")

            ### New: Handling Constants (int, float) ###
            elif isinstance(node.leaf, (int, float)):
                codigo.append(f"ldc {node.leaf} \t\t # Load constant {node.leaf}")
                instrucciones.append(f"ldc {node.leaf}")

            ### New: Handling Identifiers (str) ###
            elif isinstance(node.leaf, str):
                codigo.append(f"lod {node.leaf} \t\t # Load value of {node.leaf}")
                instrucciones.append(f"lod {node.leaf}")

            ### Handle Generic Nodes (No Code Generation) ###

            # Handle structural nodes like program, list_decl, list_sent, else_part, etc.
            elif tipo in {"program", "list_decl", "list_sent", "bloque", "else_part", "exp_bool_or_value", "comb", "sent", "list_id"}:
                for child in node.children:
                    procesar_nodo(child)

            # Default: skip unknown or unhandled node types
            else:
                print(f"Skipping unknown or generic node: {tipo}")

    # Start processing from the root of the AST
    procesar_nodo(node)

    # Add final instruction to stop the execution
    codigo.append("stp \t\t # Detener ejecución")
    instrucciones.append("stp")

    # Save the instructions to the output file
    with open(archivo_salida, "w") as archivo:
        archivo.write("\n".join(instrucciones) + "\n")

    # Return the code with comments for display (optional)
    return "\n".join(instrucciones)