# SplicER
 Analytic scheme for the analysis of Splicing Efficiency in RNA-seq data. This python tool will analyze RNA-seq reads overlapping a set of exon-exon junctions and classify each read as "clean" or "dirty" (see ASHG2015.Poster.final.pdf for more details).  
The user needs to provide a minimum of two inputs 1) RNA-seq alignment file in BAM format and 2) a file containing a set of junctions in junctionfile format.

You need python with the pysam module installed to run SplicER.  

Quick start: 
> python splicer.py --bamfile=alignment.bam --junctionfile=junction.txt --output=output.txt  

For more information:
> python splicer.py -h  

The --junctionfile accepts a file where each line corresponds to a junction ID in the following format:
>pos$chr1:1000  
>pos$chr1:1500  
>...  
>neg$chr:1100  
>neg$chr:1600  

The junction ID contains 3 pieces of information separated as such:
>type -"$"- chromosome -":"- position  

, where type corresponds to the position of the junction relative to the border of the exon (pos=3' & neg=5' genomic coordinates, NOT direction of transcription).  

A set of constituitive junctions for the hg19 human and mm9 mouse genomes can be found in the junctionfiles folder.  

This tool was first presented as a poster at the American Society of Human Genetics conference in Baltimore in 2015. A PDF file of this poster is included.  
