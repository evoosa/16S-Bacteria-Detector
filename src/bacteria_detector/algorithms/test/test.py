from bacteria_detector import config
import os


# TODO - queue and ram is different for some runs?
def get_run_cmd(sample_name: str):
    """ Get the command needed to run a test command on the given sample data """
    output_dir = os.path.join(config.output_dir, sample_name)
    return f'mkdir -p {output_dir}; touch {os.path.join(output_dir, sample_name + "_test")}'
