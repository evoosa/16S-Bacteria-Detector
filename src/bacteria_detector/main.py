import os
from bacteria_detector import config
from bacteria_detector.utils import get_run_on_cluster_cmd, create_directory_if_missing, prepare_for_run, run_cmd


def main():
    prepare_for_run()
    sample_dirs = os.listdir(config.DEFAULT_INPUT_DIR)
    for sample_dir in sample_dirs:
        algorithm = str(sample_dir.split('_')[-1])
        sample_name = '_'.join(sample_dir.split('_')[:-1])
        create_directory_if_missing(os.path.join(config.OUTPUT_DIR, sample_name))
        print('\n-------------------------------------------------\n')
        if algorithm in config.SUPPORTED_ALGORITHMS:
            print(f"\n'{sample_dir}' uses '{algorithm}' algorithm")
            create_directory_if_missing(os.path.join(config.OUTPUT_DIR, sample_name, algorithm))
            run_on_cluster_cmd = get_run_on_cluster_cmd(sample_name, algorithm)
            run_cmd(run_on_cluster_cmd)
        else:
            print(f"\n[XXX] '{sample_dir}' - unsupported algorithm! skipping..")


if __name__ == '__main__':
    main()
