import datetime

SUPPORTED_ALGORITHMS = ['swift', 'test']
# DEFAULT_BASE_OUTPUT_DIR = f'/home/labs/bfreich/maork/evoosa/output'
now = datetime.datetime.now().strftime("%m_%d_%Y-%H_%M")
OUTPUT_DIR = DEFAULT_BASE_OUTPUT_DIR + f'_{now}'
RUN_LOG_OUTPUT_DIR = f'{OUTPUT_DIR}_run_logs'

# Cluster Properties
DEFAULT_QUEUE = 'gromacs'  # 'public-himem'
DEFAULT_JOB_CPU = '1'
DEFAULT_JOB_MEM = '16000'

