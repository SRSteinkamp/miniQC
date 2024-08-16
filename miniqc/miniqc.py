import argparse

import bids
import matplotlib.pyplot as plt
import nibabel as nb
import numpy as np
from tqdm.auto import tqdm

from .application import App
from .fmri_plots import (
    apply_colormap_to_2d_array,
    get_middle_slice,
    mean_img,
    padding,
    padding_dims,
    std_img,
)


def create_bids_parser():
    parser = argparse.ArgumentParser(description="BIDS-compatible command line parser.")
    # Required BIDS arguments
    parser.add_argument(
        "bids_dir",
        type=str,
        help="The directory with the input dataset formatted according to the BIDS standard.",
    )
    parser.add_argument(
        "output_dir",
        type=str,
        help="The directory where the output files should be stored.",
    )
    parser.add_argument(
        "--task_id",
        type=str,
        default=None,
        help="Select a specific task to be analyzed. If this parameter is not provided all tasks should be analyzed.",
    )
    parser.add_argument(
        "--session_id",
        type=str,
        default=None,
        help="Select a specific session to be analyzed. If this parameter is not provided all sessions should be analyzed.",
    )
    parser.add_argument(
        "--run_id",
        type=str,
        default=None,
        help="Select a specific run to be analyzed. If this parameter is not provided all runs should be analyzed.",
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
        default="Greys",
        help="Specify the plot to be analyzed. Default is 'fmri'.",
    )
    return parser


def miniqc_gui():
    parser = create_bids_parser()
    args = parser.parse_args()
    print(args)
    # Print parsed arguments for debugging purposes

    print("Parsed arguments:")
    for arg in vars(args):
        print(f"{arg}: {getattr(args, arg)}")

    dict_args = vars(args)

    cmap = plt.get_cmap(args.colormap)

    if args.modality == "fmri":
        modality = "bold"

    file_filter = {
        i: dict_args[i + "_id"]
        for i in ["task", "run", "session"]
        if dict_args[i + "_id"] is not None
    }

    print(file_filter)

    bids_data = bids.BIDSLayout(args.bids_dir, validate=False)
    print(bids_data)
    bids_images = bids_data.get(suffix=modality, extension=args.extension)
    print(bids_images)
    if len(bids_images) == 0:
        raise ValueError("Something went wrong")

    image_array = {}
    for ii in tqdm(bids_images[:4], desc="loading images"):
        single_img = nb.load(ii)
        pad_dim = padding_dims(single_img)

        if args.plot == "mean":
            single_img = mean_img(single_img.get_fdata())
        elif args.plot == "std":
            single_img = std_img(single_img.get_fdata())

        # single_img = single_img / np.max(np.abs(single_img))

        single_img = apply_colormap_to_2d_array(single_img, cmap) * 255
        single_img = padding(single_img, pad_dim)

        middle_dims = get_middle_slice(single_img)

        image_array[ii.filename] = [single_img.astype(np.uint8), middle_dims]

    app = App(image_array, args.output_dir)
    app.mainloop()


if __name__ == "__main__":
    miniqc_gui()
