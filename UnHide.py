import steg as s
import sys

if len(sys.argv) ==3:
	s.UnHide(sys.argv[1],sys.argv[2])
else:
	print "Syntax Incorrect\n Decode_text [inputimage.png] [outputfilename] " 
