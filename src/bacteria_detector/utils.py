from bacteria_detector import config


def get_run_on_cluster_cmd(sample_name: str) -> str:  # FIXME - output errors to a specific dir, even log it in future
    """ Get the bsub command to run on the cluster """
    run_alg_cmd = 'CMD_TEMP'  # FIXME
    return f'bsub -q {config.DEFAULT_QUEUE} -n {config.DEFAULT_JOB_CPU} -R "rusage[mem={config.DEFAULT_JOB_MEM}]" -J {sample_name} -o {sample_name}.out -e {sample_name}.err {run_alg_cmd}'


# find "/home/labs/bfreich/shaharr/microbiome_seq_290920/raw_data/results/" -maxdepth 1 | grep swift | awk -F'[\/]' '{print("bsub -q gromacs -n 1 -R \42rusage[mem=16000]\42 -J "$NF" -o "$NF".out -e "$NF".err ./q2wkflow_v2.sh config.txt " $0" " $NF)}'

# #!/bin/bash
#
# bsub -q public-himem -n 1 -R "rusage[mem=16000]" -J WS_swift -o WS_swift.out -e WS_swift.err ./q2wkflow_v2.sh config.txt /home/labs/bfreich/shaharr/microbiome_seq_290920/raw_data/results/WS_swift WS_swift
# bsub -q public-himem -n 1 -R "rusage[mem=16000]" -J WL_swift -o WL_swift.out -e WL_swift.err ./q2wkflow_v2.sh config.txt /home/labs/bfreich/shaharr/microbiome_seq_290920/raw_data/results/WL_swift WL_swift
# bsub -q public-himem -n 1 -R "rusage[mem=16000]" -J WR_swift -o WR_swift.out -e WR_swift.err ./q2wkflow_v2.sh config.txt /home/labs/bfreich/shaharr/microbiome_seq_290920/raw_data/results/WR_swift WR_swift
# bsub -q public-himem -n 1 -R "rusage[mem=16000]" -J HVL_swift -o HVL_swift.out -e HVL_swift.err ./q2wkflow_v2.sh config.txt /home/labs/bfreich/shaharr/microbiome_seq_290920/raw_data/results/HVL_swift HVL_swift
# bsub -q new-interactive -n 1 -R "rusage[mem=40000]" -J TS_swift -o TS_swift.out -e TS_swift.err ./q2wkflow_v2.sh config.txt /home/labs/bfreich/shaharr/microbiome_seq_290920/raw_data/results/TS_swift TS_swift
# bsub -q new-interactive -n 1 -R "rusage[mem=40000]" -J 28S_swift -o 28S_swift.out -e 28S_swift.err ./q2wkflow_v2.sh config.txt /home/labs/bfreich/shaharr/microbiome_seq_290920/raw_data/results/28S_swift 28S_swift
# bsub -q public-himem -n 1 -R "rusage[mem=16000]" -J TL_swift -o TL_swift.out -e TL_swift.err ./q2wkflow_v2.sh config.txt /home/labs/bfreich/shaharr/microbiome_seq_290920/raw_data/results/TL_swift TL_swift
# bsub -q public-himem -n 1 -R "rusage[mem=16000]" -J 20_each_swift -o 20_each_swift.out -e 20_each_swift.err ./q2wkflow_v2.sh config.txt /home/labs/bfreich/shaharr/microbiome_seq_290920/raw_data/results/20_each_swift 20_each_swift
# bsub -q public-himem -n 1 -R "rusage[mem=16000]" -J TR_swift -o TR_swift.out -e TR_swift.err ./q2wkflow_v2.sh config.txt /home/labs/bfreich/shaharr/microbiome_seq_290920/raw_data/results/TR_swift TR_swift
# bsub -q public-himem -n 1 -R "rusage[mem=16000]" -J dec_swift -o dec_swift.out -e dec_swift.err ./q2wkflow_v2.sh config.txt /home/labs/bfreich/shaharr/microbiome_seq_290920/raw_data/results/dec_swift dec_swift
# bsub -q public-himem -n 1 -R "rusage[mem=16000]" -J 28L_swift -o 28L_swift.out -e 28L_swift.err ./q2wkflow_v2.sh config.txt /home/labs/bfreich/shaharr/microbiome_seq_290920/raw_data/results/28L_swift 28L_swift
# bsub -q public-himem -n 1 -R "rusage[mem=16000]" -J Mix_swift -o Mix_swift.out -e Mix_swift.err ./q2wkflow_v2.sh config.txt /home/labs/bfreich/shaharr/microbiome_seq_290920/raw_data/results/Mix_swift Mix_swift
# bsub -q public-himem -n 1 -R "rusage[mem=16000]" -J 28R_swift -o 28R_swift.out -e 28R_swift.err ./q2wkflow_v2.sh config.txt /home/labs/bfreich/shaharr/microbiome_seq_290920/raw_data/results/28R_swift 28R_swift
# bsub -q public-himem -n 1 -R "rusage[mem=16000]" -J NTC_swift -o NTC_swift.out -e NTC_swift.err ./q2wkflow_v2.sh config.txt /home/labs/bfreich/shaharr/microbiome_seq_290920/raw_data/results/NTC_swift NTC_swift
