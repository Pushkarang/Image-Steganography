import steg
import sys

if len(sys.argv) == 4:
	steg.HideThis(sys.argv[1],sys.argv[2],sys.argv[3])
else:
	print "Syntax Incorrect\n Usage Hide_file_into_img [inputimage.png] [filename] [outputfile.png]"

