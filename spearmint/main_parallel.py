from argparse import ArgumentParser
import numpy as np
from spearmint.util_parallel import parallel_execute
from spearmint.main import main


def main_parallel(expt_dir_list, repeat, load_init, num_proc, llsub_rank, llsub_size):
    worker_args = []
    worker_kwargs = []
    for expt_dir in expt_dir_list:
        worker_args.extend([(expt_dir,) for i in range(repeat)])
        worker_kwargs.extend([{'no_output': True, 'repeat': i, 'load_init': load_init} for i in range(repeat)])

    if llsub_rank is not None and llsub_size is not None: # supercloud
        worker_args = np.array_split(np.array(worker_args, dtype=object), llsub_size)[llsub_rank].tolist()
        worker_kwargs = np.array_split(np.array(worker_kwargs, dtype=object), llsub_size)[llsub_rank].tolist()

    for _ in parallel_execute(main, worker_args, worker_kwargs, num_proc=num_proc, show_progress=True):
        pass


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--expt-dir', type=str, nargs='+', required=True)
    parser.add_argument('--repeat', type=int, required=True)
    parser.add_argument('--load-init', action='store_true')
    parser.add_argument('--num-proc', type=int, default=1)
    parser.add_argument('--llsub-rank', type=int, default=None)
    parser.add_argument('--llsub-size', type=int, default=None)
    args = parser.parse_args()

    main_parallel(args.expt_dir, args.repeat, args.load_init, args.num_proc, args.llsub_rank, args.llsub_size)
