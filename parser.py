import numpy as np
import matplotlib.pyplot as plt

class minijpgparser():
	def __init__(self, filelink):
		with open(filelink, "r") as openfile:
			self.minijpgstr = openfile.read()
		self.confirmminijpg()
		self.doneH = 0
		self.Ccont, self.Dcont = "", ""
		thisblock = 8
		while thisblock != len(self.minijpgstr):
			thisblock = self.teststartbloc(thisblock)
			thisblock = self.whichblock(thisblock)
		if self.Ccont:
			print self.Ccont
		if not hasattr(self, "Htype"): #if there's no type, the type will be black and white
			self.Htype = 0
			print "No header was found, the parser will assume the pixel type is black and white"
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
			Hlen += 10**(3 - i)*ord(self.minijpgstr[startindex+i])
		Hcont = self.minijpgstr[startindex+4:startindex+4+Hlen]
		Hcont_larg = 0
		Hcont_haut = 0
		for i in range(4):
			Hcont_larg += 10**(3 - i)*ord(Hcont[i])
			Hcont_haut += 10**(3 - i)*ord(Hcont[4+i])
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
			Clen += 10**(3 - i)*ord(self.minijpgstr[startindex+i])
		Ccont = self.minijpgstr[startindex+4:startindex+4+Clen]
		self.Ccont += Ccont
		newstartindex = startindex+4+Clen
		return newstartindex

	def calcD(self, startindex):
		startindex += 1
		Dlen = 0
		for i in range(4):
			Dlen += 10**(3 - i)*ord(self.minijpgstr[startindex+i])
		startindex = startindex + 4
		self.Dcont += self.minijpgstr[startindex:startindex+Dlen]
		newstartindex = startindex + Dlen
		return newstartindex

	def whichblock(self, startbloc):
		if self.minijpgstr[startbloc] == "H" and not self.doneH:
			newstartbloc = self.calcH(startbloc)
			self.doneH = 1
		elif self.minijpgstr[startbloc] == "C":
			newstartbloc = self.calcC(startbloc)
			self.doneC = 1
		elif self.minijpgstr[startbloc] == "D":
			newstartbloc = self.calcD(startbloc)
			self.doneD = 1
		else:
			raise NameError("File not structured correctly")
		return newstartbloc

	def createimagematrix(self):
		if self.Htype == 0:
			if not self.Dcont: #if no data is defined, just return the black matrix
				self.finalimage = [[0 for i in range(self.largeur)] for j in range(self.hauteur)]
				print "No data was found, the black matrix of the specified dimensions will be printed"
				return
			if not hasattr(self, "hauteur") or not hasattr(self, "largeur"): #if it doesn't have an attribute, just choose
				self.largeur = 8 #8 and the data length as the dimensions
				self.hauteur = len(self.Dcont)
			elif self.largeur*self.hauteur < 8*len(self.Dcont): #if I can complete the image by adding rows or columns, I do it
				diff = 8*len(self.Dcont) - self.largeur*self.hauteur #if not, I use 8 and the data length as the dimensions
				if diff % self.largeur == 0:
					toadd = diff/self.largeur
					self.hauteur += toadd
				elif diff % self.hauteur == 0:
					toadd = diff/self.hauteur
					self.largeur += toadd
				else:
					self.largeur = 8
					self.hauteur = len(self.Dcont)
			elif self.largeur*self.hauteur > 8*len(self.Dcont): #if I can create the correct image size by adding rows or columns,
				diff = self.largeur*self.hauteur - 8*len(self.Dcont) #I do it, if not, I just leave it as it is
				if diff % self.largeur == 0:
					toremove = diff/self.largeur
					self.hauteur -= toremove
				elif diff % self.hauteur == 0:
					toremove = diff/self.hauteur
					self.largeur -= toremove
			self.finalimage = [[0 for i in range(self.largeur)] for j in range(self.hauteur)]
			return
		elif self.Htype == 1: # still have to fix problematic cases as with 1
			self.finalimage = [[0 for i in range(self.largeur)] for j in range(self.hauteur)]
			return
		elif self.Htype == 2: # still have to fix problematic cases as with 1
			self.finalimage = [[0 for i in range(self.largeur)] for j in range(self.hauteur)]
			return
		elif self.Htype == 3: # still have to fix problematic cases as with 1
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
			for i in range(self.hauteur):
				for j in range(self.largeur):
					if cont < len(allbits): #if we reached the end of data, just leave 0's
						self.finalimage[i][j] = allbits[cont]
						cont += 1
					else:
						break
			return
		elif self.Htype == 1:
			allbytes = map(ord, self.Dcont)
			cont = 0
			for i in range(self.hauteur):
				for j in range(allbytes):
					if cont < len(self.Dcont): #if we reached the end of data, just leave 0's
						self.finalimage[i][j] = allbytes[cont]
						cont += 1
					else:
						break
		elif self.Htype == 2:
			raise NameError("Not implemented yet")
		elif self.Htype == 3:
			ordDcont = map(ord, self.Dcont)
			rgb = [[ordDcont[i], ordDcont[i+1], ordDcont[i+2]] for i in range(0, len(ordDcont), 3)]
			print rgb, self.finalimage
			cont = 0
			for i in range(self.hauteur):
				for j in range(self.largeur):
					if cont < len(rgb): #if we reached the end of data, just leave 0's
						self.finalimage[i][j] = rgb[cont]
						cont += 1
					else:
						break
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
		elif self.Htype == 2:
			raise NameError("Not implemented yet")
		elif self.Htype == 3:
			aux = np.array(self.finalimage)
			aux = aux.astype(np.uint8)
			print aux
			plt.imshow(aux)
			plt.show()
			return
		else:
			raise NameError("Non existent pixel type")

	def teststartbloc(self, startbloc): #here I just keep going until I find a block, I could also raise an error
		while startbloc < len(self.minijpgstr) and self.minijpgstr[startbloc] not in ["H", "C", "D"]:
			startbloc += 1
		return startbloc

def main():
	filelink = raw_input("Type here the minipng file you want to parse: \n")
	parsedimage = minijpgparser(filelink)
	return

main()