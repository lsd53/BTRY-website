file = open("Yeastgeneinfo.txt",'r')
file_write = open("geneinfo.txt",'w')

for l in file:
	line=l.split()
	string = line[1]+ '\t' +line[2]+'\t'+line[3]+' \n'
	file_write.write(string)
