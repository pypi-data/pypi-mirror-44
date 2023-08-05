#!/home/liaoth/tools/miniconda2/envs/tmap_beta/bin/python
import argparse
import pickle
import warnings

from tmap.api.general import *
from tmap.tda.plot import vis_progressX, Color

warnings.filterwarnings('ignore')


def main(args):
    graph = pickle.load(open(args.graph, 'rb'))
    accessory_objs = graph['accessory_obj']
    projected_X = accessory_objs['raw_X']
    color = None
    if args.metadata:
        metadata = data_parser(args.metadata)
        col = args.column
        if not col:
            logger("No column assign, it won't assign any color.", verbose=1)

        else:
            col_data = metadata.loc[:, col]
            color = Color(col_data, dtype=args.dtype, target_by='sample')

    vis_progressX(graph,
                  projected_X=projected_X,
                  mode='file',
                  simple=False if args.complex else True,
                  color=color,
                  filename=args.output,
                  auto_open=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-G", "--graph", help="Graph file computed from 'Network_generator.py'.",
                        type=str, required=True)
    parser.add_argument("-O", "--output", help="full path of output file",
                        type=str, required=True)
    parser.add_argument("-M", "--metadata", help="full path of metadata",
                        type=str, )
    parser.add_argument("-col", "--column", help="column you want to use as color with", type=str)
    parser.add_argument("-t", "--dtype", help="column you want to use as color with", type=str, default='numerical')
    parser.add_argument("--complex", help="increase graph complexity",
                        action="store_true")
    args = parser.parse_args()

    process_output(output=args.output)

    main(args)
