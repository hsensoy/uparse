import sys

if sys.argv[1].lower() == '-u':	# Cast to upper case
	print " ".join(t.upper() for t in sys.argv[2:])
elif sys.argv[1].lower() == '-l':	# Cast to lower case
	print " ".join(t.lower() for t in sys.argv[2:])
elif sys.argv[1].lower() == '-ic':	# Cast to inicap/title case
	print " ".join(t.title() for t in sys.argv[2:])
else:
	print >> sys.stderr, "Unsupported cast flag. Use one of -u: upper -l:lower or -ic: initcap"

