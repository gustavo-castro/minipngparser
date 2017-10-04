minipng = open('./minipngimages/A.mp', 'r')
ministr = minipng.read()

if ministr[:9] != "Mini-PNGH":
	print "deu ruim"
else:
	index = 9
	Hlen = 0
	for i in range(4):
		Hlen += 10**(3 - i)*ord(ministr[index+i])
	Hcont = ministr[13:13+Hlen]
	Hcont_larg = 0
	Hcont_haut = 0
	for i in range(4):
		Hcont_larg += 10**(3 - i)*ord(Hcont[i])
		Hcont_haut += 10**(3 - i)*ord(Hcont[4+i])
	Htype = ord(Hcont[-1])
	auxdict = {0:"noir et blanc", 1:"niveaux de gris", 2:"palette", 3:"coleurs 24 bits"}
	print "Largeur: ", Hcont_larg, "Hauteur: ", Hcont_haut, "Pixel type: ", auxdict[Htype]
	index = 13+Hlen+1
	Clen = 0
	for i in range(4):
		Clen += 10**(3 - i)*ord(ministr[index+i])
	Ccont = ministr[index+4:index+4+Clen]
	print Ccont
	index = index+4+Clen+1
	Dlen = 0
	for i in range(4):
		Dlen += 10**(3 - i)*ord(ministr[index+i])
	finalimage = [[0 for i in range(Hcont_larg)] for j in range(Hcont_haut)]
	index = index + 4
	Dcont = ministr[index:]
	if Hcont_larg*Hcont_haut != 8*Dlen:
		print "deu ruim"
	else:
		allbits = ""
		for c in Dcont:
			auxbin = bin(ord(c))[2:]
			lenaux = len(auxbin)
			if lenaux < 8:
				for i in range(8 - lenaux):
					auxbin = "0" + auxbin
			allbits += auxbin
		cont = 0
		for i in range(Hcont_haut):
			for j in range(Hcont_larg):
				finalimage[i][j] = allbits[cont]
				cont += 1
		for line in finalimage:
			print "".join(map(lambda x:" " if x=="1" else "X", line))