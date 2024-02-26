#!/bin/zsh

# This file contains the minimum configuration 
# to execute wcsim_root_to.C binary


# Only root is needed
module add Analysis/root/6.24.06

# Set wcsim path
wcsim_bin_path=/sps/t2k/bquilain/HK/Reconstruction/official_2023/Gonzalo/WCSim-1.12.8/WCSim_build/mydir/bin
source ${wcsim_bin_path}/this_wcsim.sh

# Informative display
