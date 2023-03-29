from argparse import ArgumentParser

def getFlagObj():
    parser = ArgumentParser()
    #parser.add_argument("-d", "--device",     dest="model", required=True, help="Specify device model.")
    parser.add_argument("-i", "--input",      dest="configPath",  default="config.json", help="Specifies path of config.json file.")
    parser.add_argument("-o", "--output",     dest="outputPath",  default="", help="Specify output directory.")
    return parser.parse_args()