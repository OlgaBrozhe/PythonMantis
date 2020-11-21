from model.project_form import ProjectForm
import random
import string
import os.path
import jsonpickle
import getopt
import sys


def genereate():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "n:f:", ["number of projects", "file"])
    except getopt.GetoptError as err:
        getopt.usage()
        sys.exit(2)

    n = 5
    f = "data/projects.json"

    for o, a in opts:
        if o == "-n":
            n = int(a)
        elif o == "-f":
            f = a

    # Create random data
    def random_string(prefix, maxlen):
        # Picking symbols for random choice: ascii_letters, digits, punctuation and a number spaces
        # symbols = string.ascii_letters + string.digits + string.punctuation + " "*10
        symbols = string.ascii_letters + string.digits + " " * 10
        # Random choice of symbols, generated for cycle of random length, not higher than max length
        list_random_symbols = [random.choice(symbols) for i in range(random.randrange(maxlen))]
        random_string_from_symbols_list = prefix + "".join(list_random_symbols)
        return random_string_from_symbols_list

    testdata = [ProjectForm(project_name=random_string("Project__", 10),
                            project_description=random_string("Description__", 10)) for i in range(n)]
    data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), f)
    # What to do with the opened file:
    with open(data_file, "w") as file_out:
        jsonpickle.set_encoder_options("json", indent=2)
        file_out.write(jsonpickle.encode(testdata))
