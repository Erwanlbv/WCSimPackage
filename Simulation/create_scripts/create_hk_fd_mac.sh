#!/bin/bash


# Define environment variables with default values

save_path=${save_path:-"/sps/t2k/eleblevec/datasets/wcsimroot_datasets/hk/test/electron.mac"}
root_file=${root_file:-"/sps/t2k/eleblevec/datasets/wcsimroot_datasets/hk/test/default_hk_mac_test.root"}
verbose=${verbose:-0}
seed=${seed:-100}


particle=${particle:-"e-"}

# Keep -1 as default value for the unwanted configuration (mono vs spectrum)
mono_energy=${mono_energy:--1}
min_energy=${min_energy:-100}
max_energy=${max_energy:-1000}

beamOn=${beamOn:-10}


# Start generating the .mac file
echo "# Sample setup macro with no visualization" > $save_path

# Add the core content to $save_path using echo
echo "/run/verbose $verbose" >> $save_path
echo "/tracking/verbose 0" >> $save_path
echo "/hits/verbose 0" >> $save_path
echo "/grdm/verbose 0" >> $save_path

# Detector geometry
echo "/WCSim/SetPMTPercentCoverage 20.2150576375662" >> $save_path
echo "/WCSim/SetPMTPercentCoverage2 0." >> $save_path
echo "/WCSim/WCgeom HyperK_HybridmPMT_WithOD" >> $save_path
echo "/WCSim/Construct" >> $save_path

echo "/WCSim/PMTQEMethod SensitiveDetector_Only" >> $save_path
echo "/WCSim/PMTCollEff on" >> $save_path
echo "/WCSim/SavePi0 false" >> $save_path
echo "/DAQ/Digitizer SKI" >> $save_path
echo "/DAQ/Trigger NDigits" >> $save_path
echo "/control/execute macros/daq.mac" >> $save_path

# Dark Rate configuration
echo "/DarkRate/SetDetectorElement tank" >> $save_path
echo "/DarkRate/SetDarkMode 1" >> $save_path
echo "/DarkRate/SetDarkWindow 4000" >> $save_path
echo "/mygen/generator gps" >> $save_path

# Particule configuration
echo "/gps/particle $particle" >> $save_path
echo "/gps/pos/type Volume" >> $save_path
echo "/gps/pos/shape Cylinder" >> $save_path
echo "/gps/pos/halfz 32.8755 m" >> $save_path
echo "/gps/pos/radius 32.4 m" >> $save_path
echo "/gps/ang/type iso" >> $save_path

# Energy configuration 
if (( $mono_energy > 0 )); then
    echo "/gps/ene/type Mono" >> $save_path
    echo "/gps/ene/mono $mono_energy MeV" >> $save_path
elif (( $min_energy >= 0 )) && (( $max_energy >= 0)); then
    echo "/gps/ene/type Lin" >> $save_path
    echo "/gps/ene/gradient 0"  >> $save_path
    echo "/gps/ene/intercept 1" >> $save_path

    echo "/gps/ene/min $min_energy MeV" >> $save_path
    echo "/gps/ene/max $max_energy MeV" >> $save_path
else 
    echo "Invalid values for mono_energy : $mono_energy or min_energy and max : ${min_energy}, ${max_energy}"
    exit 1
fi

# Seed and output file configuration
echo "/WCSim/random/seed $seed" >> $save_path
echo "/WCSimIO/RootFile $root_file" >> $save_path

# Number of events to run
echo "/run/beamOn $beamOn" >> $save_path

# Make it accessible
chmod u+x $save_path

echo "$save_path has been created."