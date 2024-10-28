. ~/adaptive/readfish/bin/activate
which readfish
python -m minknow_api.examples.manage_simulated_devices --add MS00000
cd /opt/ont/minknow/bin
sudo systemctl stop minknow
sudo ./mk_manager_svc -c /opt/ont/minknow/conf --simulated-minion-devices=1 &
cd -

# in a separate terminal
# ~/Downloads/ont-dorado-server_7.2.13_linux64/ont-dorado-server/bin/dorado_basecall_server --port 5555 --log_path ~/adaptive/human_test/dorado_log --config ~/Downloads/ont-dorado-server_7.2.13_linux64/ont-dorado-server/data/dna_r9.4.1_450bps_fast.cfg --device "cuda:0"

# launch minknow, set up the sequencing run
# sudo chmod -R 777 /var/lib/minknow/

## PRIMERS TEST
# edit ~/adaptive/adatest/adatest.toml
# cd ~/adaptive/adatest/
# readfish validate adatest.toml
# readfish targets --toml adatest.toml --device MS00000 --log-file adaptive_readfish.log --experiment-name adatest

## HUMAN CHROMOSOME 1 TEST
# edit ~/adaptive/human_test/human_chr_selection.toml
# cd ~/adaptive/human_test
# readfish validate human_chr_selection.toml

# readfish targets --toml human_chr_selection.toml --device MS00000 --log-file test.log --experiment-name test

# wait for the run to finish, then basecall the raw reads, then collect the stats
# to check the stats:
# readfish stats --toml human_chr_selection.toml --fastq-directory /var/lib/minknow/data/test2/test2/20240123_1704_MS00000_test2_36d56b1f/basecalling/pass/
