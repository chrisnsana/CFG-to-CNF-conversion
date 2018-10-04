# CFG-to-CNF-conversion
A small code project written in Python to illustrate the conversion of arbitrary context-free grammars (CFG) to equivalent context-free grammars in Chomsky normal form (CNF). 

To perform a conversion of a CFG to CNF follow these easy steps:

1) Put the json file representing the CFG you want to convert into the resources folder. There is an example CFG provided in this folder already. You can use this example to figure out the correct format.

2) Run the "run.py" script located in the root directory of the project (you should run this from this location and not somewhere else).

3) This script will prompt you which CFG you want to convert. Assuming that your json file is in the resources folder, you just have to enter its name. For example: CFG.json is located in the resources folder, so just entering CFG.json will be fine.

4) Then the script will ask you if the steps needed to convert the CFG to CNF should be written to a text file.


5) If everything went well, you can find a json file representing your CFG converted in CNF in the output folder. If you specified that the steps should be written in a text file, you will also find that text file in the output folder. If something went wrong the script should give you an error message with details.
