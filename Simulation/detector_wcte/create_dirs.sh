#!/bin/bash


export create_mac=/sps/t2k/eleblevec/cours/bash_playground/create_wcte_mac.sh
export create_slurm=/sps/t2k/eleblevec/cours/bash_playground/create_slurm.sh
export create_wcsim_execute=/sps/t2k/eleblevec/cours/bash_playground/create_wcsim_execute.sh
export create_wcsimroot_to_root=/sps/t2k/eleblevec/cours/bash_playground/create_wcsimroot_to_root.sh

export tuning_file_path=/sps/t2k/eleblevec/WCSimPackage/Simulation/detector_wcte/mac_files/tuning_parameters.mac
export source_path=/sps/t2k/eleblevec/WCSimPackage/Simulation/sh_files/wcsim_12_8.sh

base_folder_name=electron

mkdir -p $base_folder_name
cd $base_folder_name


echo -e "\n\n"
for dir in {1..1}
do
    echo -e "${dir} \n"
    mkdir -p $dir
    cd $dir
    rm -rf *
    cp $tuning_file_path .

    # Create the mac file
    export seed=${dir}
    export verbose=0
    
    export pmtqemethod=Stacking_Only
    export particle=e- #e-, mu-

    export min_energy=100
    export max_energy=1000
    export beamOn=5000

    export root_file=wcsim_WCTE_NuShort16c_SO_e_100_1000MeV_5kevents_${dir}.root 
    this_mac_path=electron.mac

    export save_path=$this_mac_path
    bash $create_mac

    # Create the config file for wcsimroot_to_root
    export verbose=1

    export event_type=1
    export max_hits_sig=10000

    current_dir=$(pwd)
    export wcsimroot_file_path=$current_dir/$root_file
    export result_file_path=$current_dir/WCTE_NuShort16c_SO_e_200_1kMeV_5kevents_${dir}.root
    this_config_path="config.txt"
    
    export save_path=$this_config_path
    bash $create_wcsimroot_to_root

    # Create the execute_wcsim file
    export mac_file=$this_mac_path
    export tuning_file=$tuning_file_path
    this_execute_wcsim_path=execute_wcsim.sh

    export save_path=$this_execute_wcsim_path
    bash $create_wcsim_execute
  
    # Create the slurm file
    export wcsim_execute=$this_execute_wcsim_path
    
    export job_name=wcte_${dir}_e
    export log_path="logfile_" # don't put the %j.log here, only the path where to store the log output"

    export mem="10G"
    export time="0-05:00"
    this_slurm_path=launch_wcsim.sh

    export save_path=$this_slurm_path
    bash $create_slurm

    # Execute the slurm job
    sbatch $save_path

    cd ../
done