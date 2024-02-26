#!/bin/zsh

# This file should be the minimal configuration needed to simulate from WCSim.


# Only geant4 and root are needed
module add Analysis/root/6.24.06
module add Modelisation/geant4/10.03.p03


# Set wcsim 1.12.8 path
export wcsim_bin_path=/sps/t2k/bquilain/HK/Reconstruction/official_2023/Gonzalo/WCSim-1.12.8/WCSim_build/mydir/bin
source ${wcsim_bin_path}/this_wcsim.sh

echo -e "\n wcsim_bin_path has been added to your paths. \n Usage of this wcsim : \n (In a terminal) - \$wcsim_bin_path <detector_file.mac> <tuning_parameters.mac> \n"
