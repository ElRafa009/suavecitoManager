import lexer
import argparse

def test_lexer(input_text, source='console'):
    lexer.lexer.input(input_text)
    tokens = []
    errors = []
    while True:
        token = lexer.lexer.token()
        if not token:
            break
        tokens.append(token)
        token.lexpos = lexer.find_column(input_text, token)
        #column = lexer.find_column(input_text, token)
        if source == 'console':
            print(f"LexToken({token.type}, '{token.value}', {token.lineno}, {token.lexpos})")
        errors = lexer.lexer.errors

    return tokens, errors

def main():
    parser = argparse.ArgumentParser(description='Lexer Test Script')
    parser.add_argument('input', type=str, help='Input text or path to input file')
    args = parser.parse_args()

    # Leer el texto de entrada desde el argumento proporcionado
    input_text = None
    try:
        # Intentar abrir el archivo si el argumento es un nombre de archivo
        with open(args.input, 'r') as file:
            input_text = file.read()
    except FileNotFoundError:
        # Si no se encuentra el archivo, se asume que el argumento es el texto de entrada directamente
        input_text = args.input

    # Ejecutar el análisis léxico
    tokens = test_lexer(input_text, source='console')

if __name__ == '__main__':
    main()
