import json


class CFG:

    def __init__(self, json_file):
        self.variables = []
        self.terminals = []
        self.productions = {}
        self.start     = ''
        self.__read_json(json_file)

    """
    Read the json that describes the CFG to set correct state of the object.
    """
    def __read_json(self, json_file):
        input_file = open(json_file, 'r')
        json_data  = json.loads(input_file.read())
        
        self.variables   = json_data["Variables"]
        self.terminals   = json_data["Terminals"]
        json_productions = json_data["Productions"]

        for entry in json_productions:
            key = entry["head"]
            val = entry["body"]
            # Create the empty list for the productions for the first time.
            if key not in self.productions:
                self.productions[key] = []
                
            self.productions[key].append(val)

        input_file.close()


a = CFG('CFG.json')
print(a.variables)
print(a.terminals)
print(a.productions)
