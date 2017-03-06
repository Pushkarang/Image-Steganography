import cv2.cv as cv

class Steg():
    def __init__(self,img_path):
     self.image = cv.LoadImage(img_path)
     self.width = self.image.width
     self.height = self.image.height
     self.channels = self.image.channels
     self.cw = 0
     self.ch = 0
     self.cc = 0

    def binary(self,value,size):
        v = bin(value)[2:]
	if len(v) > size:
	    raise OwnException,"Binary size exceeded"
	while len(v) < size:
	    v = "0"+v
	return v


    def put(self, bits): 
        for c in bits:
            val = list(self.image[self.ch,self.cw]) 
            if int(c) == 1:
                val[self.cc] = int(val[self.cc]) | 1
            else:
                val[self.cc] = int(val[self.cc]) & 254
                
            self.image[self.ch,self.cw] = tuple(val)
            self.increment() 
        
    def increment(self):
        if self.cc == self.channels-1: 
            self.cc = 0
            if self.cw == self.width-1: 
                self.cw = 0
                if self.ch == self.height-1:
                    self.ch = 0
                    
                else:
                    self.ch +=1
            else:
                self.cw +=1
        else:
            self.cc +=1
            
    def getb(self):
        v = list(self.image[self.ch,self.cw])
	return bin(int(v[self.cc]))[-1]

    def text_in_binary(self):
        bina = []
        for i in range(64):
            bina.append(self.getb())
            self.increment()
        length = int("".join(bina),2)
        bina =[]
        for i in range(length):
            tmp =[]
            for j in range(8):
                tmp.append(self.getb())
                self.increment()
            bina.append("".join(tmp))
        return bina
    
    
    def hideImage(self, imtohide,output):
        imtohide = Steg(imtohide)
        w = imtohide.width
        h = imtohide.height
        if self.width*self.height*self.channels < w*h*imtohide.channels:
            raise OwnException, "Carrier image not big enough to hold all the datas to steganography" 
        binw = self.binary(w, 16) #Width coded on to byte so width up to 65536
        binh = self.binary(h, 16)
        self.put(binw) #Put width
        self.put(binh) #Put height
        print "Wait this may take time !"
        for h in range(imtohide.height): #Iterate the hole image to put every pixel values
            for w in range(imtohide.width):
                for chan in range(imtohide.channels):

                    val = imtohide.image[h,w][chan]
                    self.put(self.binary(int(val),8))

        cv.SaveImage(output,self.image)            
    def Unhideimage(self,output):
        bina = []
        for i in range(16):
            bina.append(self.getb())
            self.increment()
        width = int("".join(bina),2)
        bina = []
        for i in range(16):
            bina.append(self.getb())
            self.increment()
        height = int("".join(bina),2)
        unhideimg = cv.CreateImage((width,height), 8, 3) #Create an image in which we will put all the pixels read
        print "Wait this may take time !"
        for h in range(height):
            for w in range(width):
                for chan in range(unhideimg.channels):
                    val = list(unhideimg[h,w])
                    b=[]
                    for i in range(8):
                    	b.append(self.getb())
                    	self.increment()
            		val[chan] = int("".join(b),2)
                    unhideimg[h,w] = tuple(val)
			
        cv.SaveImage(output,unhideimg)
		    
		    
		
        
def UnHide(image,output):
	s = Steg(image)
	b = s.text_in_binary()
	for i in range(len(b)):
		b[i] = chr(int(b[i],2))
	b = "".join(b)
	f = open(output,"wb")
	f.write(b)
	f.close()
		
def HideThis(image,file,output):
    f = open(file,"rb")
    text = f.read()
    s = Steg(image)

    if s.width*s.height*s.channels < (len(text) + 64 ):
        raise OwnException,"Text size exceeded"
    s.put(s.binary(len(text),64))
    for character in text:
        s.put(s.binary(ord(character),8))
    cv.SaveImage(output,s.image)
    
    
def ImageHide(image,inimage,output):
    s = Steg(image)
    s.HideImage(inimage,output)
def ImageUnHide(image,output):
    s = Steg(image)
    o = s.UnhideImage()
    #cv.SaveImage(output,o.image)
