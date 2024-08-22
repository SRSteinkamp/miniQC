import glob

from .application import App
from .mri_viz import load_images
from .parsers import create_glob_parser


def get_image_path_glob(args):
    if isinstance(args.globstr, str):
        images = glob.glob(args.globstr)
    else:
        images = list(set(args.globstr))

    images.sort()

    # additional filter to be sure, we are catching only files we  want
    images = [i for i in images if args.extension in i]

    return images


def miniqc_gui():
    parser = create_glob_parser()
    args = parser.parse_args()

    bids_images = get_image_path_glob(args)

    bids_images = bids_images[args.image_index_first : args.image_index_last]

    if len(bids_images) == 0:
        raise ValueError("Something went wrong")

    image_array = load_images(bids_images, args)

    app = App(image_array, args.output_dir)
    app.mainloop()


if __name__ == "__main__":
    miniqc_gui()
