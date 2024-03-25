from argparse import ArgumentParser
from spearmint.util_parallel import parallel_execute
from spearmint.main import main


def main_parallel(expt_dir_list, repeat, load_init, num_proc):
    args_list = []
    kwargs_list = []
    for expt_dir in expt_dir_list:
        args_list.extend([(expt_dir,) for i in range(repeat)])
        kwargs_list.extend([{'no_output': True, 'repeat': i, 'load_init': load_init} for i in range(repeat)])

    for _ in parallel_execute(main, args_list, kwargs_list, num_proc=num_proc, show_progress=True):
        pass


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--expt-dir', type=str, nargs='+', required=True)
    parser.add_argument('--repeat', type=int, required=True)
    parser.add_argument('--load-init', action='store_true')
    parser.add_argument('--num-proc', type=int, default=1)
    args = parser.parse_args()

    main_parallel(args.expt_dir, args.repeat, args.load_init, args.num_proc)
