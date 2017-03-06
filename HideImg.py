import steg
import sys

if len(sys.argv) ==4:
	s = steg.Steg(sys.argv[1])
	s.hideImage(sys.argv[2],sys.argv[3])
else:
	print "Syntax Error Hide_img_into_img [inputimg.png] [hidethisimg.pnh] [outputimg.png]"
