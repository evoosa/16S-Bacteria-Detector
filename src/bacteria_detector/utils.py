from bacteria_detector import config
from bacteria_detector.algorithms.swift import swift
from bacteria_detector.algorithms.test import test
import os
from bacteria_detector.algorithms.swift.swift import create_swift_conf_file


def get_run_algorithm_cmd(sample_name: str, algorithm: str) -> str:
    """ Get the command needed to run the given algorithm on the sample data """
    if algorithm == 'swift':
        return swift.get_run_cmd(sample_name)
    elif algorithm == 'test':
        return test.get_run_cmd(sample_name)
    else:
        print(f'[XXX] algorithm: "{algorithm}" not supported!')
        return ''


def get_run_on_cluster_cmd(sample_name: str, algorithm: str) -> str:
    """ Get the bsub command to run on the cluster """
    run_alg_cmd = get_run_algorithm_cmd(sample_name, algorithm)
    log_path = os.path.join(config.RUN_LOG_OUTPUT_DIR, sample_name)
    # return f'LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/labs/bfreich/maork/.conda/envs/bacteria_detector/lib/ |  bsub -q {config.DEFAULT_QUEUE} -n {config.DEFAULT_JOB_CPU} -R "rusage[mem={config.DEFAULT_JOB_MEM}]" -J {sample_name}_{algorithm} -o {log_path}.out -e {log_path}.err {run_alg_cmd}'
    return f'bsub -q {config.DEFAULT_QUEUE} -n {config.DEFAULT_JOB_CPU} -R "rusage[mem={config.DEFAULT_JOB_MEM}]" -J {sample_name}_{algorithm} -o {log_path}.out -e {log_path}.err {run_alg_cmd}'


def create_directory_if_missing(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def prepare_for_run():
    create_swift_conf_file()
    create_directory_if_missing(config.OUTPUT_DIR)
    create_directory_if_missing(config.RUN_LOG_OUTPUT_DIR)


def run_cmd(cmd):
    print(f'[---] running: "{cmd}"')
    os.system(cmd)
