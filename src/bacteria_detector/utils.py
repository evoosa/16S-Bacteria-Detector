from bacteria_detector import config


def get_run_algorithm_cmd(sample_name: str, algorithm: str) -> str:
    """ Get the command needed to run the given algorithm on the sample data """
    pass


def get_run_on_cluster_cmd(sample_name: str,
                           algorithm: str) -> str:  # FIXME - output errors to a specific dir, even log it in future
    """ Get the bsub command to run on the cluster """
    run_alg_cmd = 'CMD_TEMP'  # FIXME - get command for running the algorithm
    return f'bsub -q {config.DEFAULT_QUEUE} -n {config.DEFAULT_JOB_CPU} -R "rusage[mem={config.DEFAULT_JOB_MEM}]" -J {sample_name} -o {sample_name}.out -e {sample_name}.err {run_alg_cmd}'
