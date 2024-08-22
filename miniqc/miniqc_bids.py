import bids

from .application import App
from .mri_viz import load_images
from .parsers import create_bids_parser


def get_image_path_bids(args):
    if args.modality == "fmri":
        modality = "bold"

    dict_args = vars(args)

    file_filter = {
        i: dict_args[i + "_id"]
        for i in ["task", "run", "session", "space"]
        if dict_args[i + "_id"] is not None
    }

    bids_data = bids.BIDSLayout(args.bids_dir, validate=False)
    if len(file_filter) > 0:
        bids_images = bids_data.get(
            suffix=modality, extension=args.extension, filters=file_filter
        )
    else:
        bids_images = bids_data.get(suffix=modality, extension=args.extension)

    bids_images = [i.path for i in bids_images]

    return bids_images


def miniqc_gui():
    parser = create_bids_parser()
    args = parser.parse_args()

    bids_images = get_image_path_bids(args)

    bids_images = bids_images[args.image_index_first : args.image_index_last]

    if len(bids_images) == 0:
        raise ValueError("Something went wrong")

    image_array = load_images(bids_images, args)

    app = App(image_array, args.output_dir)
    app.mainloop()


if __name__ == "__main__":
    miniqc_gui()
