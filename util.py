from commands import *

def run_command(cmd,verbose = True):
    if verbose:
        print 'Running: "%s"' % cmd
    status, text = getstatusoutput(cmd)
    exit_code = status >> 8 # high byte
    signal_num = status % 256 # low byte
    if verbose:
        print 'Status: x%04x' % status
        print 'Signal: x%02x (%d)' % (signal_num, signal_num)
        print 'Exit  : x%02x (%d)' % (exit_code, exit_code)
        print 'Core? : %s' % bool(signal_num & (1 << 8)) # high bit
        print 'Output:'
        print text
        print

def secondsToStr(t):
    rediv = lambda ll,b : list(divmod(ll[0],b)) + ll[1:]
    return "%d:%02d:%02d.%03d" % tuple(reduce(rediv,[[t*1000,],1000,60,60]))
