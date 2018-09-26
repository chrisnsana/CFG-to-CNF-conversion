from CNF import CNF


if __name__ == '__main__':
    while True:
        print('Please enter the filename of the CFG that needs to be converted'
              ' to CNF.')

        filename = input()
        steps    = False

        print('Write the steps done to achieve CNF in a text file ? [y/n]')
        result   = ''
        while True:
            result = input()
            if result == 'y':
                steps = True
                break

            elif result == 'n':
                steps = False
                break

        try:
            chomsky = CNF(filename, steps)
            chomsky.write_to_json(filename)
            print('Converted grammar written to output folder.\nEnter x to exit'
                  ' or enter any other character to continue.')
            char = input()
            if char == 'x':
                break

        except Exception as e:
            print(str(e))
            
        
        
