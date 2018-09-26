import json


class CFG:
    """
    Class that represents a context-free grammar (CFG).
    """

    def __init__(self, json_file):
        """
        Constructs a CFG object by reading a json file with the expected format.

        Parameters:
            json_file: The name of which json_file we're using for construction.
        """
        self.variables   = []
        self.terminals   = []
        self.productions = {}
        self.start       = ''
        self.__read_json(json_file)
        self.__check_ambiguous_symbols()


    def __read_json(self, json_file):
        read_path  = './resources/' + json_file
        input_file = open(read_path, 'r')

            
        try:
            json_data  = json.loads(input_file.read())
            
            self.variables   = json_data["Variables"]
            self.terminals   = json_data["Terminals"]
            json_productions = json_data["Productions"]
            self.start       = json_data["Start"]

        except Exception:
            raise Exception('Invalid json file or invalid format for the CFG. '
                           'Refer to the example json for the correct format.')
            

        for entry in json_productions:
            key = entry["head"]
            val = entry["body"]
            # Create the empty list for productions on first encounter of a key.
            if key not in self.productions:
                self.productions[key] = []
                
            self.productions[key].append(val)

        input_file.close()


    def __check_ambiguous_symbols(self):
        """
        Method that checks whether a symbol is used ambiguously in the
        provided json. Using a symbol as both terminal and variable
        would be considered ambiguous and will throw an exception.
        """
        ambiguous = set()
        ambiguous.intersection(self.variables, self.terminals)
        if len(ambiguous) > 0:
            bad_symbol = ambiguous.pop()
            error_msg  = ('Provided json contains ambiguous use of the symbol '
                          + bad_symbol + '. Make sure a symbol is not both '
                          'terminal and nonterminal in the json.')
            raise Exception(error_msg)

