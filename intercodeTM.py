class InterCode:
    def __init__(self):
        self.text = ""
        self.instructions = 0
        self.freeRegister = 1

    def asignRegister(self):
        register = self.freeRegister
        self.freeRegister += 1
        return register
    
    def libRegister(self):
        self.freeRegister -= 1

    def convertir_a_tipo_correcto(self, valor):
        """Convierte el valor al tipo adecuado si es posible."""
        try:
            if isinstance(valor, str):
                if '.' in valor:
                    return float(valor)
                return int(valor)
            return valor
        except ValueError:
            return valor

    def simular_evaluar_expresion(self, expresion, symTab):
        """Simula la evaluación de las expresiones aritméticas de forma recursiva."""
        cant = 0
        if isinstance(expresion, tuple) and len(expresion) >= 3:
            operador, op1, op2, lineno = expresion

            cant += self.simular_evaluar_expresion(op1, symTab)
            cant += self.simular_evaluar_expresion(op2, symTab)

            try:
                if operador in ['+','-','*','/','<','<=','>','>=']:
                    if operador == '+':
                        return cant+1

                    elif operador == '-':
                        return cant+1

                    elif operador == '*':
                        return cant+1

                    elif operador == '/':
                        return cant+1

                    elif operador == '>':
                        return cant+1

                    elif operador == '<':
                        return cant+1

                    elif operador == '>=':
                        return cant+1

                    elif operador == '<=':
                        return cant+1                   
                    
                if operador in ['==','!=']:
                    if operador == '==':
                        return cant+1
                    elif operador == '!=':
                        return cant+1
                
                if operador in ['and', 'or']:
                    if(op1 != True and op1 != False):
                        with open("ErroresSemanticos.txt", "a") as archivo_errores:
                            archivo_errores.write(f"Error de operacón: se intenta realizar una operación booleana con numeros " + str(expresion) + "\n")
                        return 0
                    if(op2 != True and op2 != False):
                        with open("ErroresSemanticos.txt", "a") as archivo_errores:
                            archivo_errores.write(f"Error de operacón: se intenta realizar una operación booleana con numeros " + expresion + "\n")
                        return 0
                    if operador == 'and':
                        return cant+1
                    elif operador == 'or':
                        return cant+1

                return cant

            except TypeError as e:
                print(f"Error al evaluar la expresión: {e}")
                return None
        elif isinstance(expresion, (int, float, str)):
            
            if isinstance(expresion, str):
                if symTab.st_lookup(expresion) != None:
                    return cant+1
                else:
                    value = self.convertir_a_tipo_correcto(expresion)
                    if isinstance(value, int):
                        return cant+1
                    elif isinstance(value, float):
                        return cant+1
                return cant
                       
        return cant

    def evaluar_expresion(self, expresion, symTab):
        """Evalúa las expresiones aritméticas de forma recursiva."""
        if isinstance(expresion, tuple) and len(expresion) >= 3:
            operador, op1, op2, lineno = expresion

            op1 = self.convertir_a_tipo_correcto(self.evaluar_expresion(op1, symTab))
            op2 = self.convertir_a_tipo_correcto(self.evaluar_expresion(op2, symTab))

            try:
                if operador in ['+','-','*','/','<','<=','>','>=']:
                    if operador == '+':
                        self.text += str(self.instructions) + ": ADD " +  str(op1[0]) + "," + str(op1[0]) + "," + str(op2[0]) + "\n"
                        self.instructions+=1
                    elif operador == '-':
                        self.text += str(self.instructions) + ": SUB " +  str(op1[0]) + "," + str(op1[0]) + "," + str(op2[0]) + "\n"
                        self.instructions+=1
                    elif operador == '*':
                        self.text += str(self.instructions) + ": MUL " +  str(op1[0]) + "," + str(op1[0]) + "," + str(op2[0]) + "\n"
                        self.instructions+=1
                    elif operador == '/':
                        if(op1[1] == "int" and op2[1] == "int"):
                            self.text += str(self.instructions) + ": DIV " +  str(op1[0]) + "," + str(op1[0]) + "," + str(op2[0]) + "\n"
                        else:
                            self.text += str(self.instructions) + ": DVF " +  str(op1[0]) + "," + str(op1[0]) + "," + str(op2[0]) + "\n"
                        self.instructions+=1

                    elif operador == '>':
                        self.text += str(self.instructions) + ": GE " +  str(op1[0]) + "," + str(op1[0]) + "," + str(op2[0]) + "\n"
                        self.instructions+=1
                    elif operador == '<':
                        self.text += str(self.instructions) + ": LES " +  str(op1[0]) + "," + str(op1[0]) + "," + str(op2[0]) + "\n"
                        self.instructions+=1
                    elif operador == '>=':
                        self.text += str(self.instructions) + ": GEQ " +  str(op1[0]) + "," + str(op1[0]) + "," + str(op2[0]) + "\n"
                        self.instructions+=1
                    elif operador == '<=':
                        self.text += str(self.instructions) + ": LEQ " +  str(op1[0]) + "," + str(op1[0]) + "," + str(op2[0]) + "\n"
                        self.instructions+=1
                   
                    
                if operador in ['==','!=']:
                    if operador == '==':
                        self.text += str(self.instructions) + ": EQU " +  str(op1[0]) + "," + str(op1[0]) + "," + str(op2[0]) + "\n"
                        self.instructions+=1
                    elif operador == '!=':
                        self.text += str(self.instructions) + ": NEQ " +  str(op1[0]) + "," + str(op1[0]) + "," + str(op2[0]) + "\n"
                        self.instructions+=1
                
                if operador in ['and', 'or']:
                    if(op1 != True and op1 != False):
                        with open("ErroresSemanticos.txt", "a") as archivo_errores:
                            archivo_errores.write(f"Error de operacón: se intenta realizar una operación booleana con numeros " + str(expresion) + "\n")
                        return 0
                    if(op2 != True and op2 != False):
                        with open("ErroresSemanticos.txt", "a") as archivo_errores:
                            archivo_errores.write(f"Error de operacón: se intenta realizar una operación booleana con numeros " + expresion + "\n")
                        return 0
                    if operador == 'and':
                        self.text += str(self.instructions) + ": AND " +  str(op1[0]) + "," + str(op1[0]) + "," + str(op2[0]) + "\n"
                        self.instructions+=1
                    elif operador == 'or':
                        self.text += str(self.instructions) + ": OR " +  str(op1[0]) + "," + str(op1[0]) + "," + str(op2[0]) + "\n"
                        self.instructions+=1

                self.libRegister() #Free right register

                tipo = "int"

                if op1[1] == "int" and op2[1] == "int":
                    tipo = "int"
                elif op1[1] == "float" or op2[1] == "float" :
                    tipo = "float"
                else:
                    tipo = "bool"

                return (op1[0],tipo)

            except TypeError as e:
                print(f"Error al evaluar la expresión: {e}")
                return None
        elif isinstance(expresion, (int, float, str)):
            tipo = "int"
            registro = self.asignRegister()
            if isinstance(expresion, str):
                var = symTab.st_lookup(expresion)
                if var != None:
                    tipo = var['var_type']
                    self.text += str(self.instructions) + ": LD " +  str(registro) + "," + str(var['loc']) + "(0)\n"
                    self.instructions+=1
                else:
                    value = self.convertir_a_tipo_correcto(expresion)
                    if isinstance(value, int):
                        tipo = "int"
                        self.text += str(self.instructions) + ": LDC " +  str(registro) + "," + str(expresion) + "(0)\n"
                        self.instructions+=1
                    elif isinstance(value, float):
                        tipo = "float"
                        self.text += str(self.instructions) + ": LDF " +  str(registro) + "," + str(expresion) + "(0)\n"
                        self.instructions+=1
                return (registro, tipo)
                       
        return None
    
    def simulate_procesar_ast(self, nodo, symTab):
        """Procesa el AST para llenar el texto del código intermedio"""
        cant = 0
        if not nodo:
            return cant
        
            #if isinstance(nodo, str):
           # if self.buscar_variable(nodo) != None: #Si encuentra la variable en la tabla agrega el número de línea
           #     self.agregar_variable(nodo, None, None, linea_actual)
           #     if mostrar_arbol:
           #         nuevo_nodo = QTreeWidgetItem([nodo])
            #print(nodo)
            #return
            #else: #Sacar error, ya que no existe la variable
            #    with open("ErroresSemanticos.txt", "a") as archivo_errores:
            #        archivo_errores.write(f"Error en la variable: " + nodo + " se intenta acceder sin una declaración previa\n")        

        if isinstance(nodo, tuple) and len(nodo) > 0:
            tipo_nodo = nodo[0]
                
            if tipo_nodo == 'asignacion' and len(nodo) >= 4:
                
                variable = nodo[1]
                var = symTab.st_lookup(variable)
                expresion = nodo[3]
                cant += self.simular_evaluar_expresion(expresion, symTab)

                if var != None:
                    cant += 1

                for subnodo in nodo[2:]:
                    if isinstance(subnodo, (str)):
                        cant += self.simulate_procesar_ast(subnodo, symTab)
            
            elif tipo_nodo == "!=" or tipo_nodo == "==":
                cant += self.simular_evaluar_expresion(nodo, symTab)

            elif tipo_nodo == ">" or tipo_nodo == ">=" or tipo_nodo == "<" or tipo_nodo == "<=":
                cant += self.simular_evaluar_expresion(nodo, symTab)

            elif tipo_nodo == "and" or tipo_nodo == "or":
                cant += self.simular_evaluar_expresion(nodo, symTab)

            elif tipo_nodo == "+" or tipo_nodo=="-" or tipo_nodo == "*" or tipo_nodo == "/":
                cant += self.simular_evaluar_expresion(nodo, symTab)

            elif tipo_nodo == "read" or tipo_nodo == "write":
                var = symTab.st_lookup(nodo[1])
                if var != None:
                    if tipo_nodo == "read":
                        cant += 2
                    elif tipo_nodo == "write":
                        cant += 2

            # Agregar sentencias condicionales

            elif tipo_nodo == "do-until":
                
                instructions = nodo[1]
                condition = nodo[2]

                cant += self.simulate_procesar_ast(instructions, symTab)
                cant += self.simular_evaluar_expresion(condition, symTab)
                cant += 1
            
            elif tipo_nodo == "while":

                condition = nodo[1]
                instructions = nodo[2]
                
                cant += self.simular_evaluar_expresion(condition, symTab)
                cant += 1

                cant += self.simulate_procesar_ast(instructions,symTab)
                cant += 1

            elif tipo_nodo == "if":

                condition = nodo[1]
                instructions = nodo[2]
                otherclausele = nodo[3]

                cant += self.simular_evaluar_expresion(condition, symTab)
                cant += 1
                cant += self.simulate_procesar_ast(instructions, symTab)



                if(otherclausele[0] == "else"):
                    cant += 1
                    cant += self.simulate_procesar_ast(otherclausele[1], symTab)
                    cant += 1

            else:
                for subnodo in nodo[1:]:
                    if isinstance(subnodo, (tuple, list, str)):
                        cant += self.simulate_procesar_ast(subnodo, symTab)


        elif isinstance(nodo, list):
            for subnodo in nodo:
                cant += self.simulate_procesar_ast(subnodo, symTab)
        
        return cant



    def procesar_ast(self, nodo, symTab):
        """Procesa el AST para llenar el texto del código intermedio"""

        if not nodo:
            return
        
        #if isinstance(nodo, str):
           # if self.buscar_variable(nodo) != None: #Si encuentra la variable en la tabla agrega el número de línea
           #     self.agregar_variable(nodo, None, None, linea_actual)
           #     if mostrar_arbol:
           #         nuevo_nodo = QTreeWidgetItem([nodo])
            #print(nodo)
            #return
            #else: #Sacar error, ya que no existe la variable
            #    with open("ErroresSemanticos.txt", "a") as archivo_errores:
            #        archivo_errores.write(f"Error en la variable: " + nodo + " se intenta acceder sin una declaración previa\n")        

        if isinstance(nodo, tuple) and len(nodo) > 0:
            tipo_nodo = nodo[0]

                
            if tipo_nodo == 'asignacion' and len(nodo) >= 4:
                
                variable = nodo[1]
                var = symTab.st_lookup(variable)
                expresion = nodo[3]
                valor = self.evaluar_expresion(expresion, symTab)

                if var != None:
                    self.text += str(self.instructions) + ": ST " + str(valor[0]) + "," + str(var['loc']) + "(0)\n" 
                    self.instructions += 1
                    self.libRegister()

                for subnodo in nodo[2:]:
                    if isinstance(subnodo, (str)):
                        if isinstance(nodo[-1], int):
                            linea_actual = nodo[-1]
                        self.procesar_ast(subnodo, symTab)
            
            elif tipo_nodo == "!=" or tipo_nodo == "==":
                valor = self.evaluar_expresion(nodo, symTab)

            elif tipo_nodo == ">" or tipo_nodo == ">=" or tipo_nodo == "<" or tipo_nodo == "<=":
                valor = self.evaluar_expresion(nodo, symTab)

            elif tipo_nodo == "and" or tipo_nodo == "or":
                valor = self.evaluar_expresion(nodo, symTab)

            elif tipo_nodo == "+" or tipo_nodo=="-" or tipo_nodo == "*" or tipo_nodo == "/":
                valor = self.evaluar_expresion(nodo, symTab)

            elif tipo_nodo == "read" or tipo_nodo == "write":
                var = symTab.st_lookup(nodo[1])
                if var != None:
                    if tipo_nodo == "read":
                        register = self.asignRegister()
                        self.text += str(self.instructions) + ": IN " + str(register) + ",0,0\n"
                        self.instructions += 1
                        self.text += str(self.instructions) + ": ST " + str(register) + "," + str(var['loc']) + "(0)\n" 
                        self.instructions += 1
                        self.libRegister()
                    elif tipo_nodo == "write":
                        register = self.asignRegister()
                        self.text += str(self.instructions) + ": LD " +  str(register) + "," + str(var['loc']) + "(0)\n"
                        self.instructions += 1
                        self.text += str(self.instructions) + ": OUT " + str(register) + ",0,0\n" 
                        self.instructions += 1
                        self.libRegister()

            # Agregar sentencias condicionales

            elif tipo_nodo == "do-until":
                
                instructions = nodo[1]
                condition = nodo[2]

                inicio = self.instructions
                self.procesar_ast(instructions, symTab)
                valor = self.evaluar_expresion(condition, symTab)
                final = self.instructions
                self.text += str(self.instructions) + ": JEQ " + str(valor[0]) + "," + str(inicio-final-1) + "(7)\n"
                self.instructions += 1
                self.libRegister()
            
            elif tipo_nodo == "while":

                condition = nodo[1]
                instructions = nodo[2]
                
                inicio = self.instructions

                valor = self.evaluar_expresion(condition, symTab)
                saltos = self.simulate_procesar_ast(instructions, symTab)
                self.text += str(self.instructions) + ": JEQ " + str(valor[0]) + "," + str(saltos+1) + "(7)\n"
                self.instructions += 1
                self.libRegister()

                self.procesar_ast(instructions, symTab)
                final = self.instructions
                self.text += str(self.instructions) + ": JUC 0," + str(inicio-final-1) + "(7)\n"
                self.instructions += 1

            elif tipo_nodo == "if":
                print(nodo)
                condition = nodo[1]
                instructions = nodo[2]
                otherclausele = nodo[3]
                valor = self.evaluar_expresion(condition, symTab)
                saltos = self.simulate_procesar_ast(instructions, symTab)
                print(saltos)
                if(otherclausele[0] == "else"):
                    saltos += 1
                print(saltos)
                self.text += str(self.instructions) + ": JEQ " + str(valor[0]) + "," + str(saltos) + "(7)\n"
                self.instructions += 1
                self.libRegister()

                self.procesar_ast(instructions, symTab)

                if(otherclausele[0] == "else"):
                    saltos = self.simulate_procesar_ast(otherclausele[1], symTab)
                    self.text += str(self.instructions) + ": JUC 0," + str(saltos) + "(7)\n"
                    self.instructions += 1
                    self.procesar_ast(otherclausele[1],symTab)




            else:
                for subnodo in nodo[1:]:
                    if isinstance(subnodo, (tuple, list, str)):
                        self.procesar_ast(subnodo, symTab)


        elif isinstance(nodo, list):
            for subnodo in nodo:
                self.procesar_ast(subnodo, symTab)


    def generar_codigo_intermedio(self, ast, symTab):
        """Genera el código intermedio a partir del AST."""
        try:
            self.text = ""
            self.instructions = 0
            self.freeRegister = 1
            self.procesar_ast(ast, symTab)  # procesa ast
            self.text += str(self.instructions) + ": HALT 0,0,0"
            return self.text
        except IndexError as e:
            return f"Error procesando el AST: {e}"