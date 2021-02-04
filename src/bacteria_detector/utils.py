from bacteria_detector import config
from bacteria_detector.algorithms.swift import swift
from bacteria_detector.algorithms.test import test



def get_run_algorithm_cmd(sample_name: str, algorithm: str) -> str:
    """ Get the command needed to run the given algorithm on the sample data """
    if algorithm == 'swift':
        return swift.get_run_cmd(sample_name)
    elif algorithm == 'test':
        return test.get_run_cmd(sample_name)
    else:
        print(f'algorithm: "{algorithm}" not supported!')
        return ''


def get_run_on_cluster_cmd(sample_name: str, algorithm: str) -> str:
    # FIXME - output errors to a specific dir, even log it in future
    """ Get the bsub command to run on the cluster """
    run_alg_cmd = get_run_algorithm_cmd(sample_name, algorithm)
    unique_run_name = f'{sample_name}_{config.now}'
    return f'bsub -q {config.DEFAULT_QUEUE} -n {config.DEFAULT_JOB_CPU} -R "rusage[mem={config.DEFAULT_JOB_MEM}]" -J {unique_run_name} -o {unique_run_name}.out -e {unique_run_name}.err {run_alg_cmd}'



