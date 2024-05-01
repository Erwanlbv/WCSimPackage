#!/bin/bash

simulation_mac_path=${simulation_mac_path:-"/sps/t2k/eleblevec/WCSimPackage/Simulation/detector_hk/electron/electron.mac"}
detector_tuning_parameters_mac_path=${detector_tuning_parameters_mac_path:-"/sps/t2k/eleblevec/WCSimPackage/Simulation/detector_hk/extra_data/tuningNominal.mac"}


source /sps/t2k/eleblevec/WCSimPackage/Simulation/source_scripts/wcsim_12_5.sh

$wcsim_bin_path/WCSim $simulation_mac_path $detector_tuning_parameters_mac_path
