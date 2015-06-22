#!/usr/bin/python
import re
import sys
import datetime

# Define functions that perform a pattern match against a line.
# Multiple patterns can be specified, to define a group.
# A reject list can be defined which is applied if the line matches, this
# futher refines the match. See CONNECTIONS() for an example.
#
# Each function takes a line, and a pattern. find() and regex() are predefined
# functions that performs a find or a regular expression match
#
# A rule is specified from the command line, and is made up of a list of
# (function, "pattern") tuples. rules must be named with a '_rule' suffix
def Startup(line, pat):
    accept = [
        (find, "S T A R T")           # Startup
        ,(find, "S H U T D O W N")    # Shutdown
        ,(find, "| Received signal")    # received signal
        ]
    return doAccept(line, accept, None)

def Errors(line, pat):
    accept = [
        (find, "| ERROR |")           # Startup
        ,(find, "| WARNING |")    # Shutdown
        ,(find, "| CRITICAL |")    # received signal
        ]
    return doAccept(line, accept, None)

def CONNECTIONS(line, pat):
    accept = [
        (find, "CLUSTER_MGR")           # Startup
        ,(find, "CONNECTION-")    # Shutdown
        ,(regex, "session_manager_inl.h:.*:State:")   # Session state messages
        ]
    reject = [
        (find, " | LBM channel source")                           # CONNECTION-*
        ,(find, " | Connection downloaded")                       # CONNECTION-*
        ,(find, " | Listening for connection updates on topic")   # CONNECTION-*
        ,(find, " | Ignoring (and not watching)")                 # CONNECTION-*
        ,(find, " | Ignoring connection")                         # CONNECTION-*
        ,(find, " | Ignoring test connection")                    # CONNECTION-*
        ,(find, " | Ignoring disabled connection")                # CONNECTION-*
        ,(find, "Not assigned to me, ignoring state change")      # CONNECTION-*
        ,(find, "OBDL (conn id:")                                 # CONNECTION-*,  OBDL are kinda noisy
        ]
    return doAccept(line, accept, reject)


def Messages(line, pat):
    accept = [
        (find, "| ExecutionReport |")    # ExecutionReports
        ,(regex, "Send:.*35=[^0]")        # All session Send messages (Except heartbeats)
        ,(regex, "Receive:.*35=[^0]")     # All session receive messages (Except heartbeats)
        ]
    return doAccept(line, accept, None)

# Default rule for identifying which log lines are to be output
# Rules with a '_list' suffix identify lines to be output
def default_rule(line):
    accept = [
        (Startup, None)
        ,(Errors, None)
        ,(CONNECTIONS, None)
        ,(Messages, None)
        ]
    return doAccept(line, accept, None)

def default_help():
    print "    Outputs everything that is typically of interest, not including all the ttus and PDS"
    print "    startup downloads"

################################################################################
# Rules to output only ExecutionReports and send/receive data (DEBUG only)
def messages_rule(line):
    accept = [
        (Messages, None)
        ,(Startup, None)
        ]
    return doAccept(line, accept, None)

def messages_help():
    print "    Outputs all send and receive messages, and all ExecutionReports"
    print "    with the exception of heartbbearts"

#####################################################################################
def errors_rule(line):
    accept = [
        (Errors, None)
        , (Startup, None)
        ]
    return doAccept(line, accept, None)

def errors_help():
    print "    Oututs all WARNING, ERROR, and CRITICAL errors"

#############################################################################################
def connections_rule(line):
    accept = [
        (CONNECTIONS, None)
        , (Startup, None)
        , (Errors, None)
        ]
    return doAccept(line, accept, None)

def connections_help():
    print "    Outputs all CONNECTION and CLUSTER_MGR lines"

#############################################################################################
def startup_rule(line):
    accept = [
        (Startup, None)
        ]
    return doAccept(line, accept, None)

def startup_help():
    print "    Outputs all startup and shutdowns"

#############################################################################################
maxLineLength = 2048
rulelist = []

def runRule(startAtLine, infile, outfile, rule):
    currentLine = 0
    outputline = 0
    for line in infile:
        currentLine = currentLine + 1
        if (currentLine % 10000) == 0:
            sys.stderr.write("{0}/{1}\r".format(currentLine, outputline))
        if currentLine >= startAtLine:
            if rule(line):
                outputline = outputline + 1
                if len(line)>maxLineLength:
                    outfile.write("{0}: {1}...truncated\n".format(currentLine, line[:maxLineLength]))
                else:
                    outfile.write("{0}: {1}".format(currentLine, line))

# Given a rule name, get the rule
def getRuleFromName(name):
    dict = globals();
    if name+"_rule" in dict:
        return dict[name+"_rule"]
    return None

def getRuleHelpFromName(name):
    dict = globals();
    if name+"_help" in dict:
        return dict[name+"_help"]
    return None

# return a list of all available rule names
def getListOfRuleNames():
    rtn = []
    dict = globals();
    keys = dict.keys();
    for k in keys:
        pos = k.find("_rule")
        if pos >= 0:
            rtn.append(k[:pos])

    return rtn


def help():
    #print "Usage: logclean [-r=<rulename>] [-l=startline] [-t=<time>] [-c=<tz>] [infile, --]"
    print "Usage: logclean [-r=<rulename>] [-l=startline] [infile, --]"
    print "The output file name will be based on the rule being processed"
    print
    print "If -- is specified as the input, stdin will be read and stdout will be written. Only"
    print "one rule is allowed when reading from stdin."
    print
    print "-r: Specifies a rule set to be used. By default this is 'default'. New rules"
    print "    can easily be added. See the source. If 'all' is used, then all rules will be processed."
    print "    -r may be specified multiple times."
    print
    print "-l: Specify the line number to start processing from."
    #print
    #print "-t: Specify the time to start processing at"
    #print "    The format of the time is the same as the log files"
    #print
    #print "-c: Convert timestamp to the given timezone."
    #print "    Timezones are CST, CDT, EST, EDT, CEST, CEDT"
    print
    print "Each output line is preceded with the line number of the original file. This makes it easy to"
    print "locate an interesting point in the output, then locate it in the original."
    print
    print "Defined rules are:"
    ruleNames = getListOfRuleNames()
    for ruleName in ruleNames:
        print ruleName
        rhelp = getRuleHelpFromName(ruleName)
        if rhelp:
            rhelp()

def parse_timestamp(line):
    s = line[:26]
    dt = s.split(' ')
    if len(dt) >= 2:
        date = dt[0].split('-');
        time = dt[1].split(':');
        return datetime.datetime(date[0], date[1], date[2], time[0], time[1], time[2])

# Use string.find() to find a match in a line
def find(line, pat):
    if line.find(pat) >= 0:
        return True
    return False

# Use regex search() to find a match in a line
def regex(line, rx):
    if re.search(rx, line):
        return True
    return False

# Given a rule set, match the line against each rule
def doList(line, list):
    for tuple in list:
        if tuple[0](line, tuple[1]):
            return True
    return False

def doAccept(line, acceptList, rejectList):
    if rejectList == None:
        return  doList(line, acceptList)

    if doList(line, acceptList):
        if doList(line, rejectList) == False:
            return True;
    return False

if __name__ == "__main__":
    f_in = None
    f_out = None
    inname = None
    outname = None
    startAtLine = 1
    for arg in sys.argv[1:]:
        if arg == "--help":
            help()
            exit()
        if arg[:2] == "-r":
            s = arg[3:]
            if s == "all":
                rulelist = getListOfRuleNames()
            else:
                rulelist.append(s)
        elif arg[:2] == "-l":
            startAtLine = int(arg[3:])
        elif f_in == None:
            inname = arg
            if inname == '--':
                f_in = sys.stdin
                inname = 'stdin'
                f_out = sys.stdout
                outname = 'stdout'
            else:
                f_in = open(arg)
        elif f_out == None:
            outname = arg
            f_out = open(arg, "w")

    if len(rulelist) == 0:
        rulelist.append("default")

    if len(rulelist) > 1 and inname == 'stdin':
        sys.stderror.write("Only one rule can be specified when reading from stdin\n")
        exit(1)

    if inname == 'stdin':
        rule = getRuleFromName(rulelist[0])
        if rule == None:
            sys.stderror.write(ruleName + " does not exist as a rule\n")
        else:
            runRule(startAtLine, f_in, f_out, rule)
    else:
        for ruleName in rulelist:
            rule = getRuleFromName(ruleName)
            if rule == None:
                print ruleName + " does not exist as a rule"
            else:
                outname = inname + "_" + ruleName
                f_out = open(outname, "w")
                f_in.seek(0)
                runRule(startAtLine, f_in, f_out, rule)
                sys.stderr.write(outname + " written\n")
