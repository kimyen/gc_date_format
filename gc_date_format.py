import datetime
import getopt
import re
import sys
import os


second_prog = re.compile(r"\[([0-9.]+)s\]")

def main(inputfile, outputfile):
    filename = os.path.basename(inputfile)
    datetime_parts = filename.strip("gc-").strip(".log").split("_")
    time_parts = [int(x) for x in datetime_parts[0].split("-")]
    time_parts += [int(x) for x in datetime_parts[1].split("-")]
    start_date = datetime.datetime(time_parts[0], time_parts[1], time_parts[2], hour=time_parts[3], minute=time_parts[4], second=time_parts[5])
    if not outputfile:
        outputfile = inputfile + ".out"

    with open(inputfile, "r") as r, open(outputfile, "w") as w:
        for line in r:
            matched = second_prog.match(line)
            if matched:
                line_date = start_date + datetime.timedelta(seconds=float(matched.group(1)))
                w.write(line_date.isoformat()+line)
            else :
                w.write(line)


if __name__ == "__main__":
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('gc_date_format.py -i <inputfile> -o <outputfile>')
        sys.exit(2)

    inputfile = ""
    outputfile = ""
    for opt, arg in opts:
        if opt == '-h':
            print('gc_date_format.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    main(inputfile, outputfile)

