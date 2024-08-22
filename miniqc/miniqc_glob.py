import argparse
import glob

import matplotlib.pyplot as plt
from joblib import Parallel, delayed
from tqdm.auto import tqdm

from .application import App
from .fmri_plots import load_prepare_bold


def create_bids_parser():
    parser = argparse.ArgumentParser(description="Easy parser - using glob.")
    # Required BIDS arguments
    parser.add_argument(
        "globstr",
        type=str,
        help="The directory with the input dataset formatted according to the BIDS standard.",
        nargs="+",
    )
    parser.add_argument(
        "output_dir",
        type=str,
        help="The directory where the output files should be stored.",
    )
    parser.add_argument(
        "--modality",
        type=str,
        choices=["anat", "fmri"],
        default="fmri",
        help="Specify the modality to be analyzed. Default is 'fmri'.",
    )
    parser.add_argument(
        "--plot",
        type=str,
        choices=["mean", "std"],
        default="mean",
        help="Specify the plot to be analyzed. Default is 'fmri'.",
    )
    parser.add_argument(
        "--extension",
        type=str,
        default="nii.gz",
        help="Specify the plot to be analyzed. Default is 'fmri'.",
    )
    parser.add_argument(
        "--colormap",
        type=str,
        default="Greys_r",
        help="Specify the plot to be analyzed. Default is 'fmri'.",
    )
    parser.add_argument(
        "--njobs",
        type=int,
        default="5",
        help="Specify the plot to be analyzed. Default is 'fmri'.",
    )
    parser.add_argument(
        "--image_index_first",
        type=int,
        default=0,
        help="Specify the plot to be analyzed. Default is 'fmri'.",
    )
    parser.add_argument(
        "--image_index_last",
        type=int,
        default=None,
        help="Specify the plot to be analyzed. Default is 'fmri'.",
    )
    return parser


def miniqc_gui():
    parser = create_bids_parser()
    args = parser.parse_args()

    print("Parsed arguments:")
    for arg in vars(args):
        print(f"{arg}: {getattr(args, arg)}")

    cmap = plt.get_cmap(args.colormap)

    if isinstance(args.globstr, str):
        bids_images = glob.glob(args.globstr)
    else:
        bids_images = list(set(args.globstr))

    bids_images.sort()

    # additional filter to be sure, we are catching only files we  want
    bids_images = [i for i in bids_images if args.extension in i]

    bids_images = bids_images[args.image_index_first : args.image_index_last]

    if len(bids_images) == 0:
        raise ValueError("Something went wrong")

    results = Parallel(n_jobs=args.njobs)(
        delayed(load_prepare_bold)(i, cmap, args.plot)
        for i in tqdm(bids_images, desc="loading images")
    )
    image_array = {}
    for res in results:
        image_array[res[0]] = [res[1], res[2]]

    app = App(image_array, args.output_dir)
    app.mainloop()


if __name__ == "__main__":
    miniqc_gui()
