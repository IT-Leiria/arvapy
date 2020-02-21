import re


def FindLineRegExInString(string, pattern):
    if re.search(pattern, string):
        return True
    return False


def FindLineRegEx(fname, pattern):
    with open(fname) as search:
        for line in search:
            line = line.rstrip()  # remove '\n' at end of line
            if re.search(pattern, line):
                return line
    return -1


def FindLine(fname, pattern):
    with open(fname) as search:
        for line in search:
            line = line.rstrip()  # remove '\n' at end of line
            if pattern in line:
                return line
    return -1


def ReadConfigurationFile(fname):
    cfg = []
    with open(fname) as f_in:
        lines = filter(None, (line.rstrip() for line in f_in))
        for line in lines:
            line = line.strip()
            if not line.startswith("#"):
                line = line.split('#', 2)[0]
                line = line.strip()
                cfg_name = line.split(':', 2)[0]
                cfg_value = line.split(':', 2)[1]
                cfg.append([cfg_name.strip(), cfg_value.strip()])
    return cfg


def ReadConfiguration(string_list):
    cfg = []
    for line in string_list.splitlines():
        line = line.strip()
        if not line.startswith("#"):
            line = line.split('#', 2)[0]
            line = line.strip()
            cfg_name = line.split(':', 2)[0]
            cfg_value = line.split(':', 2)[1]
            cfg.append([cfg_name.strip(), cfg_value.strip()])
    return cfg


def WriteConfigurationFile(cfg, fname):
    with open(fname, 'a') as outfile:
        for row in cfg:
            if not FindLineRegExInString(str(row[1]), "\{(.*?)\}"):
                outfile.write("%s : %s\n" % (str(row[0]), str(row[1])))
