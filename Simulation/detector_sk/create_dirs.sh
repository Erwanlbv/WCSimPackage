#!/bin/bash


export create_mac=/sps/t2k/eleblevec/cours/bash_playground/create_hk_fd_mac.sh
export create_slurm=/sps/t2k/eleblevec/cours/bash_playground/create_slurm.sh
export create_wcsim_execute=/sps/t2k/eleblevec/cours/bash_playground/create_wcsim_execute.sh
export create_wcsimroot_to_root=/sps/t2k/eleblevec/cours/bash_playground/create_wcsimroot_to_root.sh

export tuning_file_path=/sps/t2k/eleblevec/WCSimPackage/Simulation/detector_hk/mac_files/tuningNominal.mac
export source_path=/sps/t2k/eleblevec/WCSimPackage/Simulation/sh_files/wcsim_12_5.sh

base_folder_name=electron

mkdir -p $base_folder_name
cd $base_folder_name

echo -e "\n\n"
for dir in {1..2}
do
    echo -e "\n ${dir}"
    mkdir -p $dir
    cd $dir
    rm -rf *
    cp $tuning_file_path .

    # Create the mac file
    export seed=${dir}
    export verbose=0
    
    export pmtqemethod=SensitiveDetector_Only # Stacking_Only, SensitiveDetector_Only
    export particle=e- #e-, mu-

    # export mono_energy=500
    export min_energy=200
    export max_energy=1000
    export beamOn=10

    export root_file=wcsim_HK_NomPMTs_SDO_e_200_1kMeV_10events_${dir}.root
    this_mac_path=electron.mac

    export save_path=$this_mac_path
    bash $create_mac

    # Create the config file for wcsimroot_to_root
    export verbose=0

    export event_type=15
    export max_hits_sig=18000

    current_dir=$(pwd)
    export wcsimroot_file_path=$current_dir/$root_file
    export result_file_path=$current_dir/HK_NomPMTs_SDO_e_200_1kMeV_10events_${dir}.root
    this_config_path="config.txt"
    
    export save_path=$this_config_path
    bash $create_wcsimroot_to_root

    # Create the execute_wcsim file (pay attention to the source file at the top)
    export mac_file=$this_mac_path
    export tuning_file=$wcte_tuning_file_path
    this_execute_wcsim_path=execute_wcsim.sh

    export save_path=$this_execute_wcsim_path
    bash $create_wcsim_execute

    # Create the slurm file
    export wcsim_execute=$this_execute_wcsim_path
    
    export job_name=wcte_${dir}_e
    export log_path="logfile_" # don't put the %j.log here, only the path where to store the log output"

    export mem="1G"
    export time="0-00:03"
    this_slurm_path=launch_wcsim.sh

    export save_path=$this_slurm_path
    bash $create_slurm

    # Execute the slurm job
    sbatch $save_path

    cd ../
done