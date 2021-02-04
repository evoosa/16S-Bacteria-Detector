from bacteria_detector import config
import os


# TODO - queue and ram is different for some runs?
def get_run_cmd(sample_name: str):
    """ Get the command needed to run a test command on the given sample data """
    output_file = os.path.join(config.OUTPUT_DIR, sample_name, "test", sample_name + "_test")
    return f'touch {output_file}'
