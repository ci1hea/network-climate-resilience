#!/bin/bash

# Request 32 gigabytes of real memory (RAM) 4 cores *4G = 16
#$ -l rmem=8G
# Request 4 cores in an OpenMP environment
#$ -pe openmp 4

# Email notifications to me@somedomain.com
#$ -M qianqian.li@sheffield.ac.uk
# Send an email when the job finishes or if it is aborted (by default no email is sent).
#$ -m bea

#$ -wd /data/cip19ql/rail_psgr_tasmax


# Load the modules required by our program
# Load the conda module
module load apps/python/conda


# activate the environment
# source ~/miniconda/etc/profile.d/conda.sh

source activate py39


# run the script..?

python /data/cip19ql/rail_psgr_tasmax/clustering/clustering_hiera.py