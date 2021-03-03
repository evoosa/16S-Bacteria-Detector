# 16S-Bacteria-Detector
Gets the frequency of bacterias for 16S RRNA sequences using the available algorithms

Installation
- python3 setup.py develop

Usage
- sign in to the cluster with Maor's user (maork)
- activate the conda env containing all the needed packages
  ```
  source activate qiime2-2020.8
  ```
- create an input directory, with subdirectories containing the input fastq files
    - for example, check this directory out
    ```
    ls /home/labs/bfreich/shaharr/Microbiome_Seq_150221/results/
    ```
- run this command to get required args
    ```
    ./runbd.sh -h
    ```
    - example command
      ```
      ./runbd.sh -i ~/evoosa/run_through_swift/results -o ~/evoosa/output -a swift
      ```
        - ~/evoosa/run_through_swift/results - directory containing samples
        - ~/evoosa/output - directory for the jobs output
        - swift - the algorithm to apply on the files

Known Issues
- cutadapt writes it's logs to the code directory
