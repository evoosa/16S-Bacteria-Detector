#!/bin/bash
## Swift Biosciences 16S Qiime 2 workflow
## Author Benli Chai & Sukhinder Sandhu 20190618
## Remember to edit/set the parameters in config_template.txt file
## Run as q2wkflow.sh config_template.txt inputDir workDir
## make sure work dir exists before running the pipeline


set -e
set -x

if [ $# -ne 3 ]
    then
       echo "q2wkflow.sh config.txt inputDir workdir"
        exit
fi
source $1  #read in configuration file
current_time=$(date "+%Y.%m.%d-%H.%M.%S")
echo "Starting time: "$current_time
inputDir=$2
WD=$(readlink -f $3) #work folder

runlog='log'
log=$runlog.$current_time

[ ! -d "$WD" ] && echo "Directory $WD does not exist, please create one..." && exit

mkdir ${WD}/Qobj #folder for all qiime2 data objects
mkdir ${WD}/Fastq #folder for intermediate fastq files
mkdir ${WD}/Export #folder to export qiime2 data object

echo "Primer file used: "$PRIMERS >> $log
echo "VSEARCH clustering identity: "$CLUSTERID >> $log

### Pre-processing step: trim the primers, merge PE files, and combine merged ### 
### and not merged files prior to importing to QIIME2's main functions        ###

## initiate the manifest file for importing to qiime2 upon completion of primer trimming the PE merging.
manifest=${WD}/manifest.tsv
printf "sample-id\tabsolute-filepath\tdirection\n" > $manifest
samplemeta=${WD}/sampleMetadata.tsv  #this is a sample metadata file, now is created to contain only sample IDs.  user should prepare sample metadata file in tsv format
printf "#SampleID\n" > $samplemeta

for R1 in ${inputDir}/*_R1_*fastq.gz; do #the input directory
    R2=${R1/_R1_/_R2_} #the path to the read 2 file
    echo $R1 >> $log
    echo $R2 >> $log
    echo

    basenameR1=${R1##*/}
    basenameR2=${R2##*/}
    prefixR1=${basenameR1%".fastq.gz"}
    prefixR2=${basenameR2%".fastq.gz"}
    trimmedR1=${WD}/Fastq/${prefixR1}"_primerTrimmed.fastq"
    trimmedR2=${WD}/Fastq/${prefixR2}"_primerTrimmed.fastq"
    untrimmedR1=${WD}/Fastq/${prefixR1}"_primerNotFound.fastq" #won't go to downstream analysis
    untrimmedR2=${WD}/Fastq/${prefixR2}"_primerNotFound.fastq" #won't go to downstream analysis
    prefix=${prefixR1%_L001_R1_*} #the sample name prefix of R1 and R2
    echo Processing ${prefix} ...

    merged=${WD}/Fastq/${prefix}"_merged.fastq"
    notMergedR1=${WD}/Fastq/${prefixR1}_"notMerged.fastq"
    notMergedR2=${WD}/Fastq/${prefixR2}_"notMerged.fastq"
    both=${WD}/Fastq/${prefix}"_mergedPlusNot.fastq"

    #PE option to trim primers off the reads
    echo
    echo Start primer trimming ...
    $CUTADAPT -e 0.10 -g file:$PRIMERS -G file:$PRIMERS \
              -o $trimmedR1 -p $trimmedR2  \
              --untrimmed-output $untrimmedR1 \
              --untrimmed-paired-output $untrimmedR2 \
              $R1 $R2 \
              --max-n 0 \
              --minimum-length $READLEN \
              >& log.${prefix}.cutadapt.txt

    #Merge paired end reads 
    echo
    echo Start merging paired end reads ...
    $VSEARCH --threads 4 \
             --fastq_mergepairs ${trimmedR1} \
             --reverse ${trimmedR2} \
             --fastqout ${merged} \
             --fastqout_notmerged_fwd $notMergedR1 \
             --fastqout_notmerged_rev $notMergedR2

    #Combine merged and unmerged read files into one. 
    #insert a '|' to make the sequence IDs unique between R1 and R2
    cat $merged $notMergedR1 $notMergedR2 |sed -e 's/ /|/g' > $both

    #Prepare the manifest file for importing to QIIME2#
    printf "${prefix}\t${both}\tjoined\n" >> $manifest
    printf "${prefix}\n" >> $samplemeta

done
	
### Import fastq files containing PE merged and not merged read as single read file to QIIME2 ####
     #for importing paired-end merged or combined 
     qiime tools import \
       	     --type 'SampleData[SequencesWithQuality]'  \
	     --input-path ${WD}/manifest.tsv  \
    	     --output-path ${WD}/Qobj/swift_joined.qza \
	     --input-format SingleEndFastqManifestPhred33V2

     ## Quality filtering
     qiime quality-filter q-score \
             --i-demux ${WD}/Qobj/swift_joined.qza \
             --o-filtered-sequences ${WD}/Qobj/swift_joined_qfilter_seq \
             --o-filter-stats ${WD}/Qobj/swift_joined_qfilter_stats 

### Starting the ASV approach
     ## Use dada2 for removal of noise including chimeras and generation of ASVs instead of clustering for OTUs
     qiime dada2 denoise-single \
             --i-demultiplexed-seqs ${WD}/Qobj/swift_joined_qfilter_seq.qza \
             --o-table ${WD}/Qobj/swift_joined_dada2_ft \
             --o-representative-sequences ${WD}/Qobj/swift_joined_dada2_rep \
             --p-trunc-len 0 \
             --o-denoising-stats ${WD}/Qobj/swift_joined_dada2_stats

     ## Classification of ASVs from dada2
     qiime feature-classifier classify-consensus-blast \
             --i-reference-reads $CLASSIFIER_seq \
             --i-reference-taxonomy $CLASSIFIER_tax \
             --i-query ${WD}/Qobj/swift_joined_dada2_rep.qza \
             --p-strand both \
             --o-classification ${WD}/Qobj/swift_joined_dada2_rep_taxonomy
     ## make barplot
     qiime taxa barplot \
             --i-table ${WD}/Qobj/swift_joined_dada2_ft.qza\
             --i-taxonomy ${WD}/Qobj/swift_joined_dada2_rep_taxonomy.qza \
             --o-visualization ${WD}/Qobj/swift_joined_dada2_barplot \
             --m-metadata-file $samplemeta

     ## Collapse ASV-based feature table by taxonomy
     qiime taxa collapse \
             --i-table ${WD}/Qobj/swift_joined_dada2_ft.qza \
             --i-taxonomy ${WD}/Qobj/swift_joined_dada2_rep_taxonomy.qza \
             --o-collapsed-table ${WD}/Qobj/swift_joined_dada2_ft_collapsed.qza \
             --p-level 6
     ## Export ASV-based feature table
     qiime tools export \
             --input-path ${WD}/Qobj/swift_joined_dada2_ft_collapsed.qza \
             --output-path ${WD}/Export/ASV

### Starting the OTU approach
     ## Dereplication of sequences with vsearch
     qiime vsearch dereplicate-sequences \
             --i-sequences ${WD}/Qobj/swift_joined_qfilter_seq.qza \
             --o-dereplicated-table ${WD}/Qobj/swift_joined_derep_table \
             --o-dereplicated-sequences ${WD}/Qobj/swift_joined_derep_seq 

     #clustering with vsearch
     qiime vsearch cluster-features-de-novo \
             --i-sequences ${WD}/Qobj/swift_joined_derep_seq.qza \
             --i-table ${WD}/Qobj/swift_joined_derep_table.qza \
             --p-perc-identity $CLUSTERID \
             --o-clustered-table ${WD}/Qobj/swift_joined_clustered_ft \
             --o-clustered-sequences ${WD}/Qobj/swift_joined_reps

     ## Uchime-denovo: chimera removal
     qiime vsearch uchime-denovo \
             --i-sequences ${WD}/Qobj/swift_joined_reps.qza \
             --i-table ${WD}/Qobj/swift_joined_clustered_ft.qza \
             --o-chimeras ${WD}/Qobj/swift_joined_chimera \
             --o-nonchimeras ${WD}/Qobj/swift_joined_nonchimera \
             --o-stats ${WD}/Qobj/unchime-denovo_stats

     ## Filter features from feature table. Here singletons and chimeras are removed
     qiime feature-table filter-features \
             --i-table ${WD}/Qobj/swift_joined_clustered_ft.qza \
             --m-metadata-file ${WD}/Qobj/swift_joined_nonchimera.qza \
             --o-filtered-table ${WD}/Qobj/swift_joined_filtered_nonchimera_ft

     ## Filter out chimeric sequences from the cluster reps
     qiime feature-table filter-seqs \
             --i-data ${WD}/Qobj/swift_joined_reps.qza \
             --m-metadata-file ${WD}/Qobj/swift_joined_nonchimera.qza \
             --o-filtered-data ${WD}/Qobj/swift_joined_reps_nonchimera

     ## Generate the summary of the feature table
     qiime feature-table summarize \
             --i-table ${WD}/Qobj/swift_joined_filtered_nonchimera_ft.qza \
             --o-visualization ${WD}/Qobj/swift_joined_table_nonchimeric.qzv

     ## Use consensus blast classifier 
     qiime feature-classifier classify-consensus-blast \
	     --i-reference-reads $CLASSIFIER_seq \
             --i-reference-taxonomy $CLASSIFIER_tax \
             --i-query ${WD}/Qobj/swift_joined_reps_nonchimera.qza \
             --p-strand both \
             --o-classification ${WD}/Qobj/swift_joined_reps_nonchimera_consensusBlast

      ## Make barplot to visualize the taxonomy annotated feature table with a user-defined sample metadata file (see: https://docs.qiime2.org/2017.12/tutorials/metadata/ for details)
      qiime taxa barplot \
             --i-table ${WD}/Qobj/swift_joined_filtered_nonchimera_ft.qza\
             --i-taxonomy ${WD}/Qobj/swift_joined_reps_nonchimera_consensusBlast.qza \
             --o-visualization ${WD}/Qobj/swift_joined_barplot \
             --m-metadata-file $samplemeta

      ## Collapse OTU-based feature table by taxonomy
      qiime taxa collapse \
             --i-table ${WD}/Qobj/swift_joined_filtered_nonchimera_ft.qza \
             --i-taxonomy ${WD}/Qobj/swift_joined_reps_nonchimera_consensusBlast.qza \
             --o-collapsed-table ${WD}/Qobj/swift_joined_filtered_nonchimera_ft_collapsed \
             --p-level 6

     ## Export OTU-based feature table
     ## Export  taxonomy of otu rep sequenes free of chimera, taxon merged
     qiime tools export \
             --input-path ${WD}/Qobj/swift_joined_filtered_nonchimera_ft_collapsed.qza \
             --output-path ${WD}/Export/OTU

     ## Enter Export folder
       cd ${WD}/Export

     ## Convert feature table from biom format to tsv format
	biom convert \
             --to-tsv \
             --input-fp ASV/feature-table.biom \
             --output-fp ASV/feature-table_ASV.tsv

	biom convert \
             --to-tsv \
             --input-fp OTU/feature-table.biom \
             --output-fp OTU/feature-table_OTU.tsv
 
    
