#!/bin/bash

#$ -N Climate_
#$ -t 1-285
#$ -o /data/cip19ql/logs
#$ -e /data/cip19ql/logs

#$ -l rmem=16G


# Email notifications
#$ -M qianqian.li@sheffield.ac.uk
# Send an email when the job finishes or if it is aborted (by default no email is sent).
#$ -m ea

#$ -wd /data/cip19ql/rail_psgr_tasmax


# Load the modules required by our program
# Load the conda module
module load apps/python/conda


# activate the environment
# source ~/miniconda/etc/profile.d/conda.sh

source activate py39


# run the script..?
#python main.py
python /data/cip19ql/rail_psgr_tasmax/climate_based.py -i $SGE_TASK_ID > output.$SGE_TASK_ID