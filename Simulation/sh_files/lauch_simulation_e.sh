#!/bin/bash

# SLURM options:

#SBATCH --job-name=e_500MeV_no_mPMTs                   # Job name
#SBATCH --output=e_500MeV_no_mPMTs%j.log             # Standard output and error log

#SBATCH --partition=htc                              # Partition choice
#SBATCH --ntasks=1                                   # Maximum number of parallel processes
#SBATCH --mem=70G                                     # Amount of memory required
#SBATCH --time=23:00:00                              # 7 days by default on htc partition

#SBATCH --mail-user=er.leblevec@gmail.com           # Where to send mail
#SBATCH --mail-type=ALL                             # Mail events (NONE, BEGIN, END, FAIL, ALL)


source /sps/t2k/eleblevec/WCSimPackage/Simulation/sh_files/wcsim_12_5.sh
$bin_path/WCSim \
    /sps/t2k/eleblevec/WCSimPackage/Simulation/mac_files/hk/e500MeV_hk.mac \
    /sps/t2k/eleblevec/WCSimPackage/Simulation/mac_files/hk/tuningNominal.mac