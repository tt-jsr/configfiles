#!/usr/bin/python

import re
import sys

REJECT = 0
ACCEPT = 1
CONTINUE = 2

# Use string.find() to find a match in a line
def faccept(line, pat):
    if line.find(pat) >= 0:
        return ACCEPT
    return CONTINUE

# Reject using find()
def freject(line, pat):
    if line.find(pat) >= 0:
        return REJECT
    return CONTINUE

# Use regex search() to find a match in a line
def raccept(line, rx):
    if re.search(rx, line):
        return ACCEPT
    return CONTINUE

# reject using regex
def rreject(line, rx):
    if re.search(rx, line):
        return REJECT
    return CONTINUE

def accept_all(line, pat):
    return ACCEPT

def reject_all(line, pat):
    return REJECT

def reject_session_manager(line, ignore_arg):
    if line.find("session_manager_inl.h") < 0:
        return CONTINUE
    if re.search("\00135=[^0]", line) > 0:
        return ACCEPT
    return REJECT

def accept_session_manager(line, ignore_arg):
    if re.search("session_manager_inl.h.*\00135=[^0]", line) > 0:
        return ACCEPT
    return CONTINUE

accept_patterns = [
    (freject, "INSTRUMENT_STORE"),
    (freject, "| lbm |"),
    (freject, "Ignoring (and not watching)"),
    (faccept, "ERROR"),
    (faccept, "CRITICAL"),
    (faccept, "WARNING"),
    (faccept, "S T A R T"),
    (faccept, "S T O P"),
    (faccept, "CLUSTER_MGR"),
    (faccept, "Requesting ttus data from url="),
    (faccept, "| STARTUP"),
    (faccept, "| CONNECTION"),
    (faccept, "| USER"),
    (faccept, "| ACCOUNT"),
    (faccept, "| SERVER"),
    (faccept, "| DIRECT"),
    (faccept, "| COMMON"),
    (faccept, "ExecutionReport"),
    (accept_session_manager, None),
    (faccept, "queue full"),
    (faccept, "is full"),
    (faccept, "==="),
    (faccept, "DownloadCompletionHandler"),
    (reject_all, None)
]

reject_patterns = [
    #(freject, "TTUS WSS"),
    (freject, "End of Transport"),
    (freject, "Beginning of Transport"),
    (reject_session_manager, None),
    (freject, "INSTRUMENT_STORE"),
    (faccept, "ERROR"),
    (faccept, "WARNING"),
    (faccept, "CRITICAL"),
    (faccept, "Requesting ttus data from url="),
    (freject, "ttus_handler.cpp"),
    (freject, "lbm_cpp.h"),
    (freject, "| lbm |"),
    (freject, "| LBM |"),
    (freject, "JSONtopb.h"),
    (freject, "| cumulus."),
    (freject, "| darwin."),
    (freject, "Ignoring (and not watching)"),
    (freject, "GetExternalMessages - Heartbeat"),
    (freject, "Cassandra upload:"),
    (freject, "| ump:"),
    (accept_all, None),
]
# Given a rule set, match the line against each rule
def doList(line, list):
    for tuple in list:
        ret = tuple[0](line, tuple[1])
        if ret != CONTINUE:
            return ret
    return REJECT

def help():
    print "filterlog [--accept | --reject] infile outfile"
    print "   --reject Use the reject patterns and only filter out lines"
    print "            explicitly matched by a pattern."
    print "            --reject is the default action."
    print "   --accept Use the accept patterns and filter out any lines"
    print "            not explicitly matched by a pattern."
    print "   infile   The name of the file for input. May be '--' for stdin."
    print "  outfile   The name of the file for output. May be '--' for stdout."

inname = None
outname = None

def main(infile, outfile, patterns):
    currentLine = 0
    outputline = 0
    outfile.write("vim:set nowrap:\n")
    outfile.write("Inputfile: {0}\n".format(inname))
    for line in infile:
        currentLine = currentLine + 1
        if (outname != 'stdout' and currentLine % 10000) == 0:
            sys.stderr.write("{0}/{1}\r".format(currentLine, outputline))
        ret = doList(line, patterns)
        if ret == ACCEPT:
            outputline = outputline + 1
            outfile.write("{0}: {1}".format(currentLine, line))

if __name__ == "__main__":
    f_in = None
    f_out = None
    patterns = reject_patterns
    for arg in sys.argv[1:]:
        if arg == "--help":
            help()
            exit()
        if arg == "--accept":
            patterns = accept_patterns
        elif arg == "--reject":
            patterns = reject_patterns
        elif f_in == None:
            if arg == '--':
                f_in = sys.stdin
                inname = 'stdin'
            else:
                f_in = open(arg)
        elif f_out == None:
            if arg == '--':
                outname = 'stdout'
                f_out = sys.stdout
            else:
                f_out = open(arg, "w")

    if f_in == None:
        f_in = sys.stdin
        inname = 'stdin'
    if f_out == None:
        outname = 'stdout'
        f_out = sys.stdout
    main(f_in, f_out, patterns)
