# SplicER
 Analytic scheme for the analysis of Splicing Efficiency in RNA-seq data. This python tool will analyze RNA-seq reads overlapping a set of junctions and classify each reads as "clean" or "dirty". The user needs to provide a RNA-seq alignment file in BAM format and a file containing a set of junctions.

Quick start: 
> python splicer.py --bamfile=alignment.bam --junctionfile=junction.txt --output=output.txt  
  
The --junctionfile accepts a file where each line corresponds to a junction ID in the following format:
>pos$chr1:1000  
>pos$chr1:1500  
>...  
>neg$chr:1100  
>neg$chr:1600  

The junction ID contains 3 pieces of information separated as such:
>type -"$"- chromosome -":"- position  

, where type corresponds to the position of the junction relative to the border of the exon (pos=3' & neg=5'). 

 I am currently configuring this github page and code will be posted soon.  
 This tool was first presented as a poster at the American Society of Human Genetics conference in Baltimore in 2015.  
