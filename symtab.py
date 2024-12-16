class LineList:
    def __init__(self, lineno):
        self.lineno = lineno
        self.next = None


class BucketList:
    def __init__(self, name, lineno, loc, var_type, value):
        self.name = name
        self.lines = LineList(lineno)
        self.memloc = loc
        self.var_type = var_type  # Tipo de la variable
        self.value = value        # Valor de la variable
        self.next = None


class SymbolTable:
    SIZE = 211
    SHIFT = 32

    def __init__(self):
        self.hash_table = [None] * self.SIZE

    def hash(self, key):
        temp = 0
        for char in key:
            temp = ((temp << self.SHIFT) + ord(char)) % self.SIZE
        #print(f"Hash: {temp}")
        return temp

    def st_insert(self, name, linenos, loc, var_type, value):
        h = self.hash(name)
        l = self.hash_table[h]

        while l is not None and l.name != name:
            l = l.next

        if l is None:  # variable not yet in table
            l = BucketList(name, linenos[0], loc, var_type, value)  # Pasar var_type y value
            l.next = self.hash_table[h]
            self.hash_table[h] = l
            
            # Agregar los otros números de línea
            for lineno in linenos[1:]:
                self.add_line_to_bucket(l, lineno)

        else:  # found in table, so just add line numbers
            for lineno in linenos:
                self.add_line_to_bucket(l, lineno)
            
            # Opcional: actualizar tipo y valor si no están definidos
            if l.var_type is None and var_type is not None:
                l.var_type = var_type
            if l.value is None and value is not None:
                l.value = value

    def add_line_to_bucket(self, bucket, lineno):
        t = bucket.lines
        while t.next is not None:
            t = t.next
        t.next = LineList(lineno)

    def st_lookup(self, name):
        h = self.hash(name)
        l = self.hash_table[h]

        while l is not None and l.name != name:
            l = l.next

        if l is None:
            return None  
        else:
            return {
                'loc': l.memloc,
                'var_type': l.var_type,
                'value': l.value
            }

    def print_sym_tab(self):
        print("Variable Name  Location   Type    Value   Line Numbers")
        print("-------------  --------   ----    -----   ------------")
        for i in range(self.SIZE):
            l = self.hash_table[i]
            while l is not None:
                t = l.lines
                line_numbers = []
                while t is not None:
                    line_numbers.append(str(t.lineno))
                    t = t.next
                print(f"{l.name:<14} {l.memloc:<8} {l.var_type if l.var_type is not None else 'N/A':<6} {l.value if l.value is not None else 'N/A':<6} {' '.join(line_numbers)}")
                l = l.next
    
    def get_sym_tab_grouped(self):
        result = []
        for i in range(self.SIZE):
            l = self.hash_table[i]
            while l is not None:
                t = l.lines
                line_numbers = []
                while t is not None:
                    line_numbers.append(str(t.lineno))
                    t = t.next
                
                # Agrupamos los números de línea en grupos de 5
                grouped_lines = []
                for i in range(0, len(line_numbers), 5):
                    grouped_lines.append(", ".join(line_numbers[i:i + 5]))
                    
                # Solo guardamos los datos para el primer grupo
                if grouped_lines:
                    first_group = grouped_lines[0]
                    result.append({
                        'name': l.name,
                        'location': l.memloc,
                        'type': l.var_type if l.var_type is not None else 'N/A',
                        'value': l.value if l.value is not None else 'N/A',
                        'lines': first_group
                    })
                    
                # Para los grupos restantes, solo guardamos ''
                for grouped in grouped_lines[1:]:
                    result.append({
                        'name': '',
                        'location': '',
                        'type': '',
                        'value': '',
                        'lines': grouped
                    })
                    
                l = l.next
        return result