import os
from bacteria_detector import config
from bacteria_detector.utils import get_run_on_cluster_cmd


def main():
    # Create the output directory
    if not os.path.exists(config.output_dir):
        os.makedirs(config.output_dir)
    sample_dirs = os.listdir(config.DEFAULT_INPUT_DIR)
    for sample_dir in sample_dirs:
        algorithm = sample_dir.split('_')[-1]
        if algorithm in config.SUPPORTED_ALGORITHMS:
            print(f"\n'{sample_dir}' uses '{algorithm}' algorithm")
            sample_name = '_'.join(sample_dir.split('_')[:-1])
            run_no_cluster_cmd = get_run_on_cluster_cmd(sample_name, algorithm)
            print(f"command to run: '{run_no_cluster_cmd}'")
        else:
            print(f"\n[XXX] '{sample_dir}' has an unsupported algorithm! skipping..")
    # run command on cluster
    # echo run results


if __name__ == '__main__':
    main()