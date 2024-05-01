#!/bin/bash

# This file contains the minimum configuration 
# to execute wcsim_root_to.C binary

module add Analysis/root/6.24.06

wcsim_bin_path=/sps/t2k/bquilain/HK/Reconstruction/official_2023/Gonzalo/WCSim-home/WCSim_build/mydir/bin
source $wcsim_bin_path/this_wcsim.sh

export convert_bin=/sps/t2k/eleblevec/WCSimPackage/Tools_WCSim_12_5/bin/wcsimroot_to_root


# ------- REMARKS -------
# --- You should not modify this file

# --- Le "module add Analysis/root/6.24.06" devrait aller chercher les trois librairies en dessous automatiquement 
# Programming_Languages/python/3.9.1
# Compilers/gcc/9.3.1
# DataManagement/xrootd/4.8.1
# --- Pour vérifier vous pouvez exécuter "module list" après avoir source ce .sh


# --- Le source exécute les 5 lignes suivantes :
# export WCSIM_BUILD_DIR=/sps/t2k/bquilain/HK/Reconstruction/official_2023/Gonzalo/WCSim-home/WCSim_build/mydir/
# export ROOT_INCLUDE_PATH=/sps/t2k/bquilain/HK/Reconstruction/official_2023/Gonzalo/WCSim-home/WCSim_build/mydir/include/WCSim:$ROOT_INCLUDE_PATH
# export PATH=/sps/t2k/bquilain/HK/Reconstruction/official_2023/Gonzalo/WCSim-home/WCSim_build/mydir/bin:$PATH
# export LD_LIBRARY_PATH=/sps/t2k/bquilain/HK/Reconstruction/official_2023/Gonzalo/WCSim-home/WCSim_build/mydir/lib:$LD_LIBRARY_PATH
# export WCSIMDIR=/sps/t2k/bquilain/HK/Reconstruction/official_2023/Gonzalo/WCSim-home/WCSim/

