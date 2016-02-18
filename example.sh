# This is an example script which will calculate counts of a and b reads
# on a subset (chr16) of the alignment produced using the Oka et al data


python splicer.py --bamfile=examples/SRR1514304.chr16.bam --junctionfile=junctionfiles/hg19.constituitive.junctions.txt --output=examples/SRR1514304.result.txt
python splicer.py --bamfile=examples/SRR1514310.chr16.bam --junctionfile=junctionfiles/hg19.constituitive.junctions.txt --output=examples/SRR1514310.result.txt
