# miniQC

miniQC is a minimalistic tool for quick quality control of
fMRI and MRI images.

The core functionality is to pre-load and possibly summarize nifti images. These are then
displayed, in a way that allows easy flipping through many participants at a time and provide
a rating of the images. These ratings can be saved to file.

The main purpose is to quickly detect images, which were incorrectly preprocessed or have major issues.

### Navigating miniQC

You can use the `left` and `right` arrow keys to flip between the different images (the filaname will be displayed).

You can use the `down` arrow key to store a reference image in the row below.

You can use `q` to rate an image as bad, `w` to rate an image as questionable (?), and `e` to rate an image as good.

Use the save button to save your ratings. If the `output_dir` argument is a directory (default `.`, i.e. the directory from which the CLI was run) the corresponding .json will be named after the current time. If `output_dir` is a filename, this will be used (make sure that the folder exist, previosu results will be overwritten with each new save).

### Example usage:

You could for example use:

`miniqc_bids path/to/bidsdir . --modality anat`

To load all anatomical images in a BIDS directory (TODO: Specify post-fix).

Alternatively:

`miniqc_glob path/to/bidsdir/sub-*/ses-*/anat/**_T1w.nii.gz . --modality anat`

Would possibly achieve the same result.

For functional data you could use

`miniqc_glob path/to/bidsdir/sub-*/ses-*/func/**_bold.nii . --modality fmri --plot std --cmap viridis --image_index_last 10 --extension .nii`

To load the first 10 images found by the function, calculate the standard deviation over time and plot these using the viridis colormap.

## Installation

You can install the package using pip:

`pip install git+https://github.com/SRSteinkamp/miniQC`

Or, for better debugging and modification clone the repository and install from there:

`git clone https://github.com/SRSteinkamp/miniQC`
`cd miniqc`
`pip install -e .`

For additional developing tools use:

`pip install -e .'[dev]'`

## Command line tools

miniQC comes with two command line tools ``miniqc_bids`` and ``miniqc_glob``.

### miniqc_glob

With `miniqc_glob` allows users to select files based on pattern matching with wildcards. This is useful when you want to target specific files across different directories without adhering to a strict data organization structure.

* **globstr**: A required argument where you specify a string with wildcards (e.g., *.nii.gz) to search for files that match this pattern.
* **output_dir**: The directory where the processed output files will be stored.

### miniqc_bids

With `miniqc_bids` `pybids` is leveraged to select files from datasets structured according to the Brain Imaging Data Structure (BIDS) standard. It allows for more detailed and specific data selection based on BIDS entities like tasks, sessions, runs, and spaces.

* `bids_dir`: A required argument specifying the directory containing the BIDS-formatted dataset.
* `output_dir`: The directory where output files should be stored.
* `--task_id`: (Optional) Filters data by a specific task. If not provided, all tasks are loaded.
* `--session_id`: (Optional) Filters data by a specific session. If not provided, all sessions are loaded.
* `--run_id`: (Optional) Filters data by a specific run. If not provided, all runs are loaded.
* `--space_id`: (Optional) Filters data by a specific space. If not provided, all spaces are loaded.

### General CLI arguments

The following optional arguments are the same across the two CLIs.

* `--modality`: Specifies the modality of the data to be analyzed. "fmri" is used for 4D NIfTI files, typically functional MRI data, while "anat" is for 3D NIfTI files, usually anatomical scans.

* `--plot`: Description: Defines how to summarize 4D NIfTI files. "mean" calculates the mean across time, while "std" computes the standard deviation. This argument is ignored for 3D files ("anat" modality).

* `--extension`: Specifies the file extension of the NIfTI files to be processed. The default is "nii.gz", commonly used for compressed NIfTI files.

* `--colormap`: Sets the colormap for visualizing the data. "Greys_r" is a reversed grayscale colormap, used by default for visualization.

* `--njobs`: Controls the number of files processed in parallel. Increasing this value can speed up processing by utilizing more CPU cores.

* `--image_index_first`: Defines the starting index for processing if only a subset of the dataset should be loaded. By default, processing starts with the first file.

* `--image_index_last`: Defines the ending index for processing if only a subset of the dataset should be loaded. If not specified, the entire dataset after the starting index will be processed.

For more details you can always use `miniqc_bids --help` or `miniqc_glob --help`.
