#!/bin/bash


# Define environment variables with default values
save_path=${save_path:-"/sps/t2k/eleblevec/datasets/wcsimroot_datasets/hk/test/wcsim_execute_hk_default.sh"}
source_path=${source_path:-"source /sps/t2k/eleblevec/WCSimPackage/Simulation/sh_files/wcsim_12_5.sh"}

mac_file=${mac_file:-"/sps/t2k/eleblevec/datasets/wcsimroot_datasets/hk/test/electron.mac"}
tuning_file=${tuning_file:-"/sps/t2k/eleblevec/WCSimPackage/Simulation/detector_hk/mac_files/tuningNominal.mac"}


# Create or overwrite $save_path
echo "#!/bin/bash" >> $save_path

echo ""
echo "source $source_path" >> $save_path
echo "\$wcsim_bin_path/WCSim $mac_file $tuning_file" >> $save_path

# Make it executable
chmod u+x $save_path

echo "$save_path has been created."
echo ""