
# import glob
# import re
# import math
# import sys
# from os import path,makedirs,chdir,getcwd,rename

def readSummaryFile(fname):
    cfgDict = {}
    with open(fname) as f_in:
        lines = filter(None, (line.rstrip() for line in f_in))
        for line in lines:
            line = line.strip()
            if not line.startswith("#"):
                #if not line == '\n' and not line == '' and not line == ' ':
                line = line.split('#', 2)[0]
                line = line.strip()
                cfg_name = line.split(':', 2)[0].strip()
                cfg_value = line.split(':', 2)[1].strip()
                cfgDict[cfg_name] = cfg_value
    return cfgDict