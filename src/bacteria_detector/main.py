import datetime
import os

from bacteria_detector.utils import get_run_on_cluster_cmd, create_directory_if_missing, prepare_for_run, \
    get_args_parser


def main(args):
    now = datetime.datetime.now().strftime("%m_%d_%Y-%H_%M")
    output_dir = os.path.join(args.output_dir, f'output_{now}')
    log_dir = os.path.join(args.output_dir, f'logs_{now}')
    prepare_for_run(args.algorithm, output_dir, log_dir)
    sample_dirs = [os.path.join(args.input_dir, o) for o in os.listdir(args.input_dir) if
                   os.path.isdir(os.path.join(args.input_dir, o))]
    for sample_dir in sample_dirs:
        sample_name = os.path.split(sample_dir)[-1]
        create_directory_if_missing(os.path.join(output_dir, sample_name))
        print(f'\n---------------------- {sample_name} ----------------------\n')
        run_on_cluster_cmd = get_run_on_cluster_cmd(sample_name, args.algorithm, log_dir, output_dir, args.input_dir)
        print(run_on_cluster_cmd)
        # run_cmd(run_on_cluster_cmd)


if __name__ == '__main__':
    args = get_args_parser()
    main(args)
