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
		self.createimage()
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
		Htype = ord(Hcont[-1])
		self.largeur, self.hauteur = Hcont_larg, Hcont_haut
		printdict = {0:"noir et blanc", 1:"niveaux de gris", 2:"palette", 3:"coleurs 24 bits"}
		print "Largeur: ", self.largeur, "Hauteur: ", self.hauteur, "Pixel type: ", printdict[Htype]
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

	def createimage(self):
		finalimage = [[0 for i in range(self.largeur)] for j in range(self.hauteur)]
		print self.largeur, self.hauteur, len(self.Dcont)
		if self.largeur*self.hauteur != 8*len(self.Dcont):
			raise NameError("Incorrect dimensions")
		else:
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
					finalimage[i][j] = allbits[cont]
					cont += 1
			self.finalimage = finalimage

	def printimage(self):
		for line in self.finalimage:
			print "".join(map(lambda x:" " if x=="1" else "X", line))

	def teststartbloc(self, startbloc):
		while startbloc < len(self.minijpgstr) and self.minijpgstr[startbloc] not in ["H", "C", "D"]:
			startbloc += 1
		return startbloc

def main():
	filelink = raw_input("Type here the minipng file you want to parse: \n")
	parsedimage = minijpgparser(filelink)
	return

main()