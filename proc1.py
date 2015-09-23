file = open("CervBinaryHQ.txt",'r')
file_write = open("interactions_pub.txt",'w')

for l in file:
	line=l.split()
	string1=line[0]+"\t"+line[1]+"\t"+line[2]+"\t"+line[3]+"\t"
	string=""
	for s in line[4:]:
		string=string+s+" " 
	string=string1+string+'\n'
	file_write.write(string)
