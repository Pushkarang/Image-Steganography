import steg
import sys

if len(sys.argv) ==3:
	s = steg.Steg(sys.argv[1])
	s.Unhideimage(sys.argv[2])
else:
	print "Syntax Error\n Decode_img [imputimage.png] [outputimage.png]"
