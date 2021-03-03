import argparse
import os

from bacteria_detector import config
from bacteria_detector.algorithms.swift import swift
from bacteria_detector.algorithms.swift.swift import create_swift_conf_file
from bacteria_detector.algorithms.test import test


def get_run_algorithm_cmd(sample_name: str, algorithm: str, output_dir: str, input_dir: str) -> str:
    """ Get the command needed to run the given algorithm on the sample data """
    if algorithm == 'swift':
        return swift.get_run_cmd(sample_name, output_dir, input_dir)
    elif algorithm == 'test':
        return test.get_run_cmd(sample_name)
    else:
        print(f'[XXX] algorithm: "{algorithm}" not supported!')
        return ''


def get_run_on_cluster_cmd(sample_name: str, algorithm: str, log_dir: str, output_dir: str, input_dir: str) -> str:
    """ Get the bsub command to run on the cluster """
    run_alg_cmd = get_run_algorithm_cmd(sample_name, algorithm, output_dir, input_dir)
    log_path = os.path.join(log_dir, sample_name)
    return f'bsub -q {config.DEFAULT_QUEUE} -n {config.DEFAULT_JOB_CPU} -R "rusage[mem={config.DEFAULT_JOB_MEM}]" -J {sample_name}_{algorithm} -o {log_path}.out -e {log_path}.err {run_alg_cmd}'


def create_directory_if_missing(dir_name: str):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def prepare_for_run(algorithm: str, output_dir: str, log_dir: str):
    """ Prepare the environment for the run """
    # create log and output dirs
    create_directory_if_missing(output_dir)
    create_directory_if_missing(log_dir)

    # create swift's config file
    if algorithm == 'swift':
        create_swift_conf_file()

    elif algorithm == 'smurf':
        pass


def run_cmd(cmd: str):
    print(f'[---] running: "{cmd}"')
    os.system(cmd)


def get_args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-dir', required=True, help='Input dir containing the samples to be processed')
    parser.add_argument('-o', '--output-dir', required=True, help='Output directory for the results and logs')
    parser.add_argument('-a', '--algorithm', required=True, help='Run samples through swift/smurf',
                        choices=['swift', 'smurf'])
    return parser.parse_args()
