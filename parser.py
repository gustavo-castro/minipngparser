import numpy as np
import matplotlib.pyplot as plt

class minijpgparser():
	def __init__(self, filelink):
		with open(filelink, "r") as openfile:
			self.minijpgstr = openfile.read()
		self.confirmminijpg()
		self.doneH = 0
		self.Ccont, self.Dcont, self.Pcont = "", "", ""
		thisblock = 8
		while thisblock != len(self.minijpgstr):
			if thisblock > len(self.minijpgstr): # here I raise an error if the letter after a block ended doesn't start another blcok
				raise NameError("Block size error")
			thisblock = self.whichblock(thisblock)
		if self.Ccont:
			print self.Ccont
		if self.Pcont:
			self.findpalette()
		if not self.Dcont:
			raise NameError("There's no data in the file")
		if not self.doneH:
			raise NameError("There's no header in the file")
		self.createimagematrix()
		self.fillimagematrix()
		self.printimage()

	def confirmminijpg(self):
		if self.minijpgstr[:8] != "Mini-PNG":
			raise NameError("Not a MiniPng file")
		else:
			return

	def calcH(self, startindex):
		startindex += 1
		Hlen = 0
		for i in range(4):
			Hlen += 256**(3 - i)*ord(self.minijpgstr[startindex+i])
		Hcont = self.minijpgstr[startindex+4:startindex+4+Hlen]
		Hcont_larg = 0
		Hcont_haut = 0
		for i in range(4):
			Hcont_larg += 256**(3 - i)*ord(Hcont[i])
			Hcont_haut += 256**(3 - i)*ord(Hcont[4+i])
		self.Htype = ord(Hcont[-1])
		self.largeur, self.hauteur = Hcont_larg, Hcont_haut
		printdict = {0:"noir et blanc", 1:"niveaux de gris", 2:"palette", 3:"coleurs 24 bits"}
		print "Largeur: ", self.largeur, "Hauteur: ", self.hauteur, "Pixel type: ", printdict[self.Htype]
		newstartindex = startindex+4+Hlen
		return newstartindex

	def calcC(self, startindex):
		startindex += 1
		Clen = 0
		for i in range(4):
			Clen += 256**(3 - i)*ord(self.minijpgstr[startindex+i])
		Ccont = self.minijpgstr[startindex+4:startindex+4+Clen]
		self.Ccont += Ccont
		newstartindex = startindex+4+Clen
		return newstartindex

	def calcD(self, startindex):
		startindex += 1
		Dlen = 0
		for i in range(4):
			Dlen += 256**(3 - i)*ord(self.minijpgstr[startindex+i])
		startindex = startindex + 4
		self.Dcont += self.minijpgstr[startindex:startindex+Dlen]
		newstartindex = startindex + Dlen
		return newstartindex

	def calcP(self, startindex):
		startindex += 1
		Plen = 0
		for i in range(4):
			Plen += 256**(3 - i)*ord(self.minijpgstr[startindex+i])
		startindex = startindex + 4
		self.Pcont += self.minijpgstr[startindex:startindex+Plen]
		newstartindex = startindex + Plen
		return newstartindex

	def findpalette(self):
		ordPcont = map(ord, self.Pcont)
		self.palette = [[ordPcont[i], ordPcont[i+1], ordPcont[i+2]] for i in range(0, len(ordPcont), 3)]
		print self.palette
		if len(self.palette) > 256:
			raise NameError("Palette is too large")

	def whichblock(self, startbloc):
		if self.minijpgstr[startbloc] == "H":
			if not self.doneH:
				newstartbloc = self.calcH(startbloc)
				self.doneH = 1
			else:
				raise NameError("More than one header")
		elif self.minijpgstr[startbloc] == "C":
			newstartbloc = self.calcC(startbloc)
		elif self.minijpgstr[startbloc] == "D":
			newstartbloc = self.calcD(startbloc)
		elif self.minijpgstr[startbloc] == "P":
			newstartbloc = self.calcP(startbloc)
		else: # here I raise an error if the letter after a block ended doesn't start another blcok
			raise NameError("File not structured correctly")
		return newstartbloc

	def createimagematrix(self):
		if self.Htype in [0,1,2]:
			self.finalimage = [[0 for i in range(self.largeur)] for j in range(self.hauteur)]
			return
		elif self.Htype == 3:
			self.finalimage = [[[0,0,0] for i in range(self.largeur)] for j in range(self.hauteur)]
			return
		else:
			raise NameError("Non existent pixel type")

	def fillimagematrix(self):
		if self.Htype == 0:
			allbits = ""
			for c in self.Dcont:
				auxbin = bin(ord(c))[2:]
				lenaux = len(auxbin)
				if lenaux < 8:
					for i in range(8 - lenaux):
						auxbin = "0" + auxbin
				allbits += auxbin
			cont = 0
			if len(allbits) < self.hauteur*self.largeur:
				raise NameError("Incorrect dimensions")
			for i in range(self.hauteur):
				for j in range(self.largeur):
					self.finalimage[i][j] = allbits[cont]
					cont += 1
			return
		elif self.Htype == 1:
			allbytes = map(ord, self.Dcont)
			cont = 0
			if len(self.Dcont) < self.hauteur*self.largeur:
				raise NameError("Incorrect dimensions")
			for i in range(self.hauteur):
				for j in range(self.largeur):
					self.finalimage[i][j] = allbytes[cont]
					cont += 1
			return
		elif self.Htype == 2:
			allbytes = map(ord, self.Dcont)
			cont = 0
			if len(allbytes) < self.hauteur*self.largeur:
				raise NameError("Incorrect dimensions")
			for i in range(self.hauteur):
				for j in range(self.largeur):
					self.finalimage[i][j] = self.palette[allbytes[cont]]
					cont += 1
			return
		elif self.Htype == 3:
			ordDcont = map(ord, self.Dcont)
			rgb = [[ordDcont[i], ordDcont[i+1], ordDcont[i+2]] for i in range(0, len(ordDcont), 3)]
			cont = 0
			if len(rgb) < self.hauteur*self.largeur:
				raise NameError("Incorrect dimensions")
			for i in range(self.hauteur):
				for j in range(self.largeur):
					self.finalimage[i][j] = rgb[cont]
					cont += 1
			return
		else:
			raise NameError("Non existent pixel type")


	def printimage(self):
		if self.Htype == 0:
			for line in self.finalimage:
				print "".join(map(lambda x:" " if x=="1" else "X", line))
			return
		elif self.Htype == 1:
			plt.imshow(self.finalimage, cmap="gray")
			plt.show()
			return
		elif self.Htype in [2,3]:
			aux = np.array(self.finalimage)
			aux = aux.astype(np.uint8)
			plt.imshow(aux)
			plt.show()
			return
		else:
			raise NameError("Non existent pixel type")

def main():
	filelink = raw_input("Type here the minipng file you want to parse: \n")
	parsedimage = minijpgparser(filelink)
	return 	

main()