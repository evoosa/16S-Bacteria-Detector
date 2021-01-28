import datetime

SUPPORTED_ALGORITHMS = ['swift']
# DEFAULT_INPUT_DIR = '/home/labs/bfreich/shaharr/microbiome_seq_290920/raw_data/results'
DEFAULT_INPUT_DIR = r'C:\Users\Maor\Documents\results'
# DEFAULT_OUTPUT_DIR = './bacteria_detector_output'
DEFAULT_BASE_OUTPUT_DIR = r'.\bacteria_detector_output'
now = datetime.datetime.now().strftime("%m_%d_%Y-%H_%M")
output_dir = DEFAULT_BASE_OUTPUT_DIR + f'_{now}'

# Cluster Properties
DEFAULT_QUEUE = 'gromacs'  # 'public-himem'
DEFAULT_JOB_CPU = '1'
DEFAULT_JOB_MEM = '16000'
