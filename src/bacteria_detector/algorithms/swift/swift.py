from bacteria_detector import config
import os


def get_run_cmd(sample_name: str):
    """ Get the command needed to run swift's algorithm on the given sample data """
    output_dir = os.path.join(config.DEFAULT_OUTPUT_DIR, sample_name)
    return f'mkdir {output_dir}; ./q2wkflow_v2.sh ./config/config.txt {os.path.join(config.DEFAULT_INPUT_DIR, sample_name)} {output_dir}'
print(get_run_cmd('dddd'))