#!/usr/bin/python
#-------------------------------------
print "Content-type: text/html"
print
#-------------------------------------
import sys
sys.stderr = sys.stdout
from cgi import escape, FieldStorage
import cgitb
cgitb.enable()
import MySQLdb
mydb = MySQLdb.connect(
	host="localhost",
	user= "lsd53",
	passwd="6VXE9A",
	db="LSD53_db")
cursor = mydb.cursor()

#get input from form
form = FieldStorage()
query = form.getfirst('protein',"")
name_type= form.getfirst('name_type',"")

#query the database for protein information
if name_type =="Entrez Gene Id":
	command='select * from genes where entrez_gene_id = "%s"; ' % query
	cursor.execute(command)
	rows=cursor.fetchall()
elif name_type=="Gene Name":
	command='select * from genes where gene_name = "%s";' % query
	cursor.execute(command)
	rows=cursor.fetchall()
else: 
	command='select * from genes where ORF = "%s";' % query
	cursor.execute(command)
	rows=cursor.fetchall()

protein_info=""
#find all interactions of the queried protein if we found the protein in the db
if rows:
	ncbi_link='''"http://www.ncbi.nlm.nih.gov/gene/?term={0}"'''.format(rows[0][0])
	protein_info='''<h2 style="text-align:center font-weight:100;">Queried protein gene name:{0}</h2>
			<p style="text-align:center;">ORF: {1} Entrez_gene_id: {2}</p>
<a href={3}>NCBI link for protein</a>
'''.format(rows[0][1], rows[0][2],rows[0][0],ncbi_link)
	gene_name=rows[0][1]
	command='select * from interactions where gene1="%s" or gene2="%s";' % (gene_name,gene_name)
	cursor.execute(command)
	interactions=cursor.fetchall()
	body=""
	number=0
	for inter in interactions:
		number=number+1
		if inter[2]==gene_name:
			interactor=inter[3]
			orf=inter[1]
		else:
			interactor=inter[2]
			orf=inter[0]
		cursor.execute('select * from genes where gene_name="%s"'% interactor)
		gene_interactor=cursor.fetchall()
		if gene_interactor:
			entrez=gene_interactor[0][0]
		else:
			entrez='Not Found'
		entrez_link='''
		<a href={0}>{1}</a>'''.format('''"http://www.ncbi.nlm.nih.gov/gene/?term={0}"'''.format(entrez),entrez)
		
		#orf=gene_interactor[0][2]
		body=body+'''
			<tr>
				<td>%d</td>
				<td>%s</td>
				<td>%s</td>			
				<td>%s</td>
				<td>%s</td>
			<tr>'''% (number,interactor,orf,entrez_link,inter[4])
		

	table='''
	<table class="pure-table" style="margin-left:auto ; margin-right:auto;">
		<thead>
			<tr>
				<th>#</th>
				<th>Gene</th>
				<th>ORF name</th>
				<th>Entrez Gene ID</th>
				<th>Publications of support</th>
			</tr>
		</thead>
		<tbody>%s
		</tbody>	
		</table>''' % body

	#if no interactions exist
	if not interactions:
		table='''<h3 style="text-align:center;">No interactions found for protein</h3>'''

#if protein does not exist in database
else:
	protein_info='''<h2>Queried protein does not exist search again</h2>'''
	table=''''''

print '''
<!DOCTYPE html>
<html>
<head style="height: 100%;"><link rel="stylesheet" href="/~lsd53/pure-min.css">
    
</head><body style="height: 100%;">
    <div style="padding: 1.3em; background: none repeat scroll 0% center rgb(170, 204, 216);" class="pure-menu pure-menu-horizontal">
        <a href="/~lsd53/home.html" class="pure-menu-heading pure-menu-link">Main</a>
        <ul class="pure-menu-list">
            <li class="pure-menu-item"><a href="/~lsd53/about.html" class="pure-menu-link">About</a></li>
        </ul>
    </div>
    <div style="" class="pure-g">
	<div class="pure-u-1-5">
	</div>
	<div class="pure-u-3-5">
		<h1 style="font-family: &quot;Raleway&quot;,&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif; text-align: center; font-weight: 100; border-bottom: 1px solid rgba(23, 26, 38, 0.44); color: rgb(18, 32, 62); font-size: 220%;">Protein Interactions</h1><h1>
	</h1></div>
    </div>
    <div class="pure-u-1-5">
    </div>
    <div class="pure-u-1-1" style="text-align: center; padding-bottom:15px;">
	{1}
    </div>
    <div class="pure-u-1-1" style="margin-bottom:25px;">
    {0} 
    </div>



<div style="bottom:0px; background-color: rgb(18, 32, 62); width: 100%; position: absolute;" id="footer">

        <p style="color: rgb(255, 255, 255); font-family: &quot;Raleway&quot;,&quot;Helvetica Neue&quot;,Helvetica,Arial,sans-serif; font-weight: 100; vertical-align: middle; position: relative; line-height: 58px; font-size: 120%; height: 100%; text-align: center; width: 100%;">Created by Luis De Medeiros using pure CSS</p>
  
  
</div>

  
</body></html>
'''.format(table,protein_info)


#:print interactions
