#!/usr/bin/python

import pysam
import sys
import re
import getopt


try:
	opts, args = getopt.getopt(sys.argv[1:],"hi:o:",["ignoreDuplicates","bamfile=","junctionfile=","output="])
except getopt.GetoptError as err:
	print (err)
	print 'Usage:'
	print '\t'+'spliceEff.py --bamfile/--samfile <Alignmemt file> --junctionfile <Junction file>'
	sys.exit(2)
ignDups=False
for opt, arg in opts:
	if opt == '-h':
		print '\n'
		print 'Usage:'
		print '\t'+'python spliceEff.py --bamfile <test.bam> --junctionfile <junctions.txt>'
		print '\n'
		print 'Required parameters:'
		print '\t'+'--bamfile/--samfile'
		print '\t\t'+'Read alignment file in SAM or BAM format'
		print '\t'+'--junctions'
		print '\t\t'+'This file needs to contain the junction information in the following format: pos/neg "$" chr ":" position.'
		print '\n'
		print 'Optional parameters:'
		print '\t'+'--ignoreDuplicates'
		print '\t\t'+'Duplicate reads will be excluded from the analysis.'
		print '\t'+'--reads <Read file>'
		print '\t\t'+'Individual read information will be saved to additonal file.'
		print '\t'+'--output <Output prefix>'
		print '\t\t'+'Results will be saved to file/s containing this prefix.'
		
		sys.exit()
	if opt =='--ignoreDuplicates':
		ignDups=True
	elif opt in ("--bamfile"):
		baminput=arg
		bamfile=pysam.AlignmentFile(baminput,"rb")
	elif opt in ("--samfile"):
		baminput=arg
		bamfile=pysam.AlignmentFile(baminput,"r")
	elif opt in ("--junctionfile"):
		junctionfile=arg
		junctions=[]
		for line in open(junctionfile,"r").readlines():
        		junctions.append(line[0:-1])
	elif opt in ("--output"):
		output=arg

#elif opt in ('--reads'):
#		readFile=arg

fileout=open(output,"w")

for item in junctions:
	#Extract pos/neg, chr and position
	side = item.split("$")[0]
	tmp = item.split("$")[1].split(":")
	position = tmp[1]
	if side =="pos":
		coord = int(position)
	else:
		coord = int(position)+1
	chr = tmp[0]
	region = str(chr)+":"+str(position)+"-"+str(position)
	ende_final=[]
	x=0
	for read in bamfile.fetch(region=region):
		cigar=read.cigarstring
		flag=int(read.flag)
		pos=read.reference_start+1
		sta=[]
		sto=[]
		loc=0
		if cigar == "75M":
			sta=[0]
			sto=[75]
		else:
			parts=[]
			tmp=0
			for m in re.finditer("[A-Z]",cigar):
				parts.append(cigar[tmp:m.end(0)])
				tmp=m.end(0)
			for p in parts:
				if "M" in p:
					sta.append(loc)
					loc=loc+int(re.split("[A-Z]",p)[0])
					sto.append(loc)
				if "D" in p:
					loc=loc+int(re.split("[A-Z]",p)[0])
				if "S" in p:
					loc=loc
				if "I" in p:
					loc=loc
				if "N" in p:
					loc=loc+int(re.split("[A-Z]",p)[0])
		starts=[]
		for i in sta:
			starts.append(int(i)+pos)
		stops=[]
		for i in sto:
			stops.append(int(i)+pos-1)
		if side =="pos":
			if stops[-1] == coord: 
				ende="NA"
			else:
				tmp=[]
				for i in starts:
					if i <= coord:
						tmp.append(i)
				if len(tmp) == 0:
					ende="NA"
				else:
					ende=stops[starts.index(max(tmp))]
		if side =="neg":
			if starts[0] == coord:
				ende="NA"
			else:
				tmp=[]
				for i in stops:
					if i >= coord:
						tmp.append(i)
				if len(tmp) == 0:
					ende="NA"
				else:
					ende=starts[stops.index(min(tmp))]
		
		if ignDups:
			if flag>=1024:
				ende="NA"	
		ende_final.append(ende)
		#print str(cigar)+"\t"+str(pos)+"\t"+str(coord)+"\t"+str(ende)+"\t"+str(flag)	
	tmp=[]
	if side =="pos":
		for i in ende_final:
			if i !="NA":
				if (int(i)-coord) > 0:
					tmp.append(1)
				if (int(i)-coord) ==0:
					tmp.append(0)
	else:
		for i in ende_final:
			if i !="NA":
				if (int(i)-coord) < 0:
					tmp.append(1)
				if (int(i)-coord) ==0:
					tmp.append(0)
	fileout.writelines(str(item)+"\t"+str(len(tmp)-sum(tmp))+"\t"+str(sum(tmp))+'\n')

