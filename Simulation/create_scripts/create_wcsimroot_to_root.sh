#!/bin/bash

save_path=${save_path:-"/sps/t2k/eleblevec/datasets/wcsimroot_datasets/hk/test/default_config.txt"}
wcsimroot_file_path=${wcsimroot_file_path:- "/sps/t2k/eleblevec/datasets/wcsimroot_datasets/hk/test/default_hk_mac_test.root"}
result_file_path=${result_file_path:- "/sps/t2k/eleblevec/datasets/wcsimroot_datasets/hk/test/default_root_file.root"}

verbose=${verbose:-0}

event_type=${event_type:-1}
max_hits_sig=${max_hits_sig:-10000}


echo "# Configuration file for wcsimroot_to_root " >> $save_path
echo "" >> $save_path

echo "WCSIMROOT_FILE_PATH=$wcsimroot_file_path" >> $save_path
echo "RESULT_FILE_PATH=$result_file_path" >> $save_path
echo "" >> $save_path

echo "################" >> $save_path
echo "## PARAMETERS ##" >> $save_path
echo "################" >> $save_path


echo "EVENT_TYPE=$event_type" >> $save_path
echo "MAX_HITS_SIG=$max_hits_sig" >> $save_path

echo "VERBOSE=$verbose" >> $save_path

# Make it accessible
chmod u+x $save_path

echo "config.txt has been created."
echo ""


