#! /bin/bash


### Set your variables here
save_path=${save_path:-"launch_sim.sh"}
wcsim_execute=${wcsim_execute:-"/sps/t2k/eleblevec/WCSimPackage/Simulation/sh_files/execute_wcte_sim.sh"}

job_name=${job_name:-"e_500_Mev"}
log_path=${log_path:-"/sps/t2k/eleblevec/cours/tests/"}

mem=${mem:-"10G"}
time=${time:-"0-00:03"}


### Start writing to $save_path
echo "#!/bin/bash" > $save_path

# Append SLURM options and other content to $save_path
echo "" >> $save_path
echo "# SLURM options:" >> $save_path
echo "" >> $save_path
echo "#SBATCH --job-name=${job_name}         " >> $save_path
echo "#SBATCH --output=${log_path}%j.log     " >> $save_path

echo "" >> $save_path
echo "#SBATCH --partition=htc                " >> $save_path
echo "#SBATCH --ntasks=1                     " >> $save_path
echo "#SBATCH --mem=${mem}                   " >> $save_path
echo "#SBATCH --time=${time}                 " >> $save_path

echo "" >> $save_path
echo "#SBATCH --mail-user=er.leblevec@gmail.com   " >> $save_path
echo "#SBATCH --mail-type=ALL                     " >> $save_path

echo "" >> $save_path
echo "bash ${wcsim_execute}" >> $save_path

# Make $save_path executable
chmod +x $save_path

echo "$save_path has been created."
echo ""
