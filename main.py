from lexer import lexer
from parser import Parser
from codegen import CodeGenerator
from evaluator import Evaluator

def main():
    # Step 1: Read input from file
    with open('input.txt', 'r') as file:
        input_code = file.read()

    # Step 2: Lexical analysis (Tokenization)
    tokens = lexer(input_code)
    
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    print (f"tokens: {tokens}")

    # Step 3: Parsing
    parser = Parser(tokens)
    parse_tree = parser.parse()
    
    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n")
    print(f"parse_tree: {parse_tree}")

    # Step 4: Code generation
    code_generator = CodeGenerator(parse_tree)
    three_address_code = code_generator.generate_code()

    # Step 5: Output three-address code to file (output.txt)
    with open('output.txt', 'w') as file:
        for line in three_address_code:
            file.write(line + '\n')

    # Step 6: Evaluate and print results
    evaluator = Evaluator('input.txt')
    results = evaluator.evaluate()
    
    print("\n++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    
    print("\nEvaluation Results:")

    for result in results:
        print(result)

if __name__ == '__main__':
    main()

