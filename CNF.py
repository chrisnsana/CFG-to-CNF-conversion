from CFG import CFG
import os


class CNF(CFG):
    """
    Class that represents a context-free grammar in Chomsky normal form (CNF).
    """

    def __init__(self, json_file, generate_steps):
        """
        Constructs a CNF object by reading a json file with the expected format.

        Parameters:
            json_file: The name of which json_file we're using for construction.
            generate_steps: Boolean indicating if we the constructor should
                            create an output file with all the steps needed
                            to convert to Chomsky normal form.
                            True generates the file, False does not.
        """
        # Construct the context-free grammar as described in the file before
        # the conversion to Chomsky normal form happens.
        super().__init__(json_file)
        self.generate_steps = generate_steps
        self.output_file    = None
        if generate_steps is True:
            # Get the file name without the path or extension (i.e. XXX.json)
            in_name  = os.path.splitext(os.path.basename(json_file))[0]
            # A simple text file will be created show casing all the steps.
            out_name = in_name + '_steps.txt'
            self.output_file = open(out_name, 'w')

        # Perform the necessary steps to achieve Chomsky normal form.
        

        


    def __write_step(self, step_description):
        # There's no output file and therefore nothing to do.
        if self.output_file is None:
            return


    def __eliminate_epsilon_transitions(self):
        """
        Eliminate all the epsilon rules, which are rules of the form A -> Ɛ
        (with A not being the start symbol of the grammar).
        """


    def __eliminate_unit_productions(self):
        """
        Eliminate all the unit productions. These are productions of the form
        A -> B with A and B being variables of the grammar.
        """

    def __eliminate_useless_symbols(self):
        """
        Eliminate all the useless symbols. There are two categories of useless
        symbols: the variables that never lead to any terminals and the symbols
        that can't be reached from the start symbol with the present production
        rules.
        """


