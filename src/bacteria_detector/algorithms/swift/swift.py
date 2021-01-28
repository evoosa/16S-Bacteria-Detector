from bacteria_detector import config


def get_run_cmd(sample_name: str):
    """ Get the command needed to run swift's algorithm on the given sample data """
    return f'./q2wkflow_v2.sh ./config/config.txt {config.DEFAULT_INPUT_DIR}/WS_swift {config.DEFAULT_OUTPUT_DIR}/WS_swift'
