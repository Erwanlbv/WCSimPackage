#!/bin/bash

# Define environment variables with default values
save_path=${save_path:-"/sps/t2k/eleblevec/cours/tests/electron.mac"}
root_file=${root_file:-"/sps/t2k/eleblevec/cours/tests/default_wcte_mac_test.root"}
seed=${seed:-2}
verbose=${verbose:-0}


pmtqemethod=${pmtqemethod:-"Stacking_Only"}
particle=${particle:-"mu-"}

min_energy=${min_energy:-100}
max_energy=${max_energy:-1000}

beamOn=${beamOn:-100}


# Create or overwrite $save_path
echo "# nuPRISMBeamTest WCTE macro with no visualization" > $save_path

# Add the content to $save_path using echo with environment variables
echo "/run/verbose $verbose" >> $save_path
echo "/tracking/verbose 0" >> $save_path
echo "/hits/verbose 0" >> $save_path
echo "/WCSim/WCgeom nuPRISMBeamTest_16cShort_mPMT ## this is 16c4r from CAD" >> $save_path
echo "/WCSim/Geometry/RotateBarrelHalfTower true" >> $save_path
echo "/WCSim/PMT/ReplicaPlacement false" >> $save_path
echo "/WCSim/PMT/PositionVariation 0 mm" >> $save_path
echo "/WCSim/PMT/TankRadiusChange 0 0 0 mm" >> $save_path
echo "/WCSim/PMT/PositionFile /sps/t2k/bquilain/HK/Reconstruction/official_2023/Gonzalo/WCSim-1.12.8/WCSim_build/mydir/data/mPMT_Position_WCTE.txt" >> $save_path
echo "/WCSim/Construct" >> $save_path
echo "/WCSim/PMTQEMethod $pmtqemethod" >> $save_path
echo "/WCSim/PMTCollEff on" >> $save_path
echo "/WCSim/SavePi0 false" >> $save_path
echo "/DAQ/Digitizer SKI" >> $save_path
echo "/DAQ/Trigger NDigits" >> $save_path
echo "/control/execute macros/daq.mac" >> $save_path
echo "/DarkRate/SetDarkMode 1" >> $save_path
echo "/DarkRate/SetDarkHigh 100000" >> $save_path
echo "/DarkRate/SetDarkLow 0" >> $save_path
echo "/DarkRate/SetDarkWindow 4000" >> $save_path
echo "/mygen/generator gps" >> $save_path
echo "/gps/particle $particle" >> $save_path
echo "/gun/position 0 0 0 m" >> $save_path
echo "/gps/ene/type Lin" >> $save_path
echo "/gps/ene/gradient 0" >> $save_path
echo "/gps/ene/intercept 1" >> $save_path
echo "/gps/ene/min $min_energy MeV" >> $save_path
echo "/gps/ene/max $max_energy MeV" >> $save_path
echo "/gps/ang/type iso" >> $save_path
echo "/gps/ang/mintheta 0 deg" >> $save_path
echo "/gps/ang/maxtheta 180 deg" >> $save_path
echo "/gps/ang/minphi 0 deg" >> $save_path
echo "/gps/ang/maxphi 360 deg" >> $save_path
echo "/Tracking/fractionOpticalPhotonsToDraw 0.0" >> $save_path
echo "/WCSimIO/RootFile $root_file" >> $save_path
echo "/WCSimIO/SaveRooTracker 0" >> $save_path
echo "/WCSim/random/seed $seed" >> $save_path
echo "/run/beamOn $beamOn" >> $save_path

# Make it accessible
chmod u+x $save_path


echo "$save_path has been created."
