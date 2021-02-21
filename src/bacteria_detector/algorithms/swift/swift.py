from bacteria_detector import config
import os

swift_script_dir = os.path.dirname(os.path.realpath(__file__))
swift_config_dir = os.path.join(swift_script_dir, 'config')
config_file_path = os.path.join(swift_script_dir, "config", "config.txt")


def create_swift_conf_file():
    """ Create swift's config file """
    config_params = f"""
    #!/usr/bash 
    CUTADAPT=~/.conda/envs/qiime2-2020.8/bin/cutadapt
    VSEARCH=~/.conda/envs/qiime2-2020.8/bin/vsearch
    PRIMERS={swift_config_dir}/primers_16S_V1-9_anchored.fasta
    READLEN=130
    CLUSTERID=0.97
    CLASSIFIER_seq={swift_config_dir}/silva_132_99_16S.qza
    CLASSIFIER_tax={swift_config_dir}/consensus_taxonomy_7_levels.qza
    """
    with open(config_file_path, 'w') as config_file:
        config_file.write(config_params)
    print(f'[---] Created swift\'s config file in "{config_file_path}" ')


def get_run_cmd(sample_name: str):
    """ Get the command needed to run swift's algorithm on the given sample data """
    output_dir = os.path.join(config.OUTPUT_DIR, sample_name, 'swift')
    input_dir = os.path.join(config.DEFAULT_INPUT_DIR, sample_name + "_swift")
    swift_script_path = os.path.join(swift_script_dir, "q2wkflow_v2.sh")
    return f'{swift_script_path} {config_file_path} {input_dir} {output_dir}'
