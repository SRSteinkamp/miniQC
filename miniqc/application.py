import datetime
import json
import os
import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk


def rgb_2_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)


class App(tk.Tk):
    def __init__(self, data_dict, output=None):
        super().__init__()

        self.title("miniQC - v0.0.1")
        self.gen_height = 900
        self.gen_width = 1600
        self.geometry(f"{self.gen_width}x{self.gen_height}")
        self.resizable(False, False)

        self.labels = list(data_dict.keys())
        self.output = output

        self.ratings = {la: "None" for la in self.labels}

        self.image_height = (self.gen_height - 200) // 2
        self.image_width = (self.gen_width - 180) // 3

        self.columnconfigure(0, weight=1, minsize=100)
        self.columnconfigure(1, weight=5, minsize=self.image_width)
        self.columnconfigure(2, weight=5, minsize=self.image_width)
        self.columnconfigure(3, weight=5, minsize=self.image_width)
        self.columnconfigure(4, weight=1, minsize=80)

        self.rowconfigure(0, weight=1, minsize=150)
        self.rowconfigure(1, weight=3, minsize=self.image_height)
        self.rowconfigure(2, weight=1, minsize=50)
        self.rowconfigure(3, weight=3, minsize=self.image_height)

        self.subject_label = ttk.Label(
            self, text="First image", font=("TkDefaultFont", 25)
        )
        self.subject_label.grid(
            row=0, column=1, padx=10, pady=10, columnspan=2, sticky="w"
        )

        self.rating_label = tk.Label(
            self,
            text="Rating:\nNone",
            bg=rgb_2_hex((75, 75, 75)),
            height=80,
            width=100,
            font=("TkDefaultFont", 25),
        )
        self.rating_label.grid(row=0, column=3, padx=20, pady=20)

        self.reference_label = ttk.Label(
            self, text="Reference:", font=("TkDefaultFont", 25)
        )
        self.reference_label.grid(
            row=2, column=1, padx=10, pady=10, columnspan=2, stick="W"
        )

        self.save_button = ttk.Button(self, text="Save", command=self.save_results)
        self.save_button.grid(row=3, column=0, padx=10, pady=10)
        # Initialize variables
        self.data_dict = data_dict
        self.index = 0

        self.color_dict = {
            "Bad": rgb_2_hex((252, 141, 98)),
            "?": rgb_2_hex((255, 217, 47)),
            "Good": rgb_2_hex((102, 194, 165)),
            "None": "white",
        }

        # Create labels to display the three planes
        self.label_xy = ttk.Label(self)
        self.label_xy.grid(row=1, column=1, padx=5, pady=5)

        self.label_yz = ttk.Label(self)
        self.label_yz.grid(row=1, column=2, padx=5, pady=5)

        self.label_xz = ttk.Label(self)
        self.label_xz.grid(row=1, column=3, padx=5, pady=5)

        self.ref_xy = ttk.Label(self)
        self.ref_xy.grid(row=3, column=1, padx=5, pady=5)

        self.ref_yz = ttk.Label(self)
        self.ref_yz.grid(row=3, column=2, padx=5, pady=5)

        self.ref_xz = ttk.Label(self)
        self.ref_xz.grid(row=3, column=3, padx=5, pady=5)

        # Bind left and right arrow keys to methods
        self.bind("<Left>", self.previous_image)
        self.bind("<Right>", self.next_image)
        self.bind("<Down>", self.save_reference)
        self.bind("q", self.bad_rating)
        self.bind("w", self.neutral_rating)
        self.bind("e", self.good_rating)

        # Display the initial images for each plane
        self.update_images()

    def update_images(self):
        # Get the current slices from the numpy array

        tmp_image, tmp_slice = self.data_dict[self.labels[self.index]]

        image_xy = tmp_image[tmp_slice[0], :, ::-1].transpose([1, 0, 2])  # XY plane
        image_yz = tmp_image[:, tmp_slice[1], ::-1].transpose([1, 0, 2])  # YZ plane
        image_xz = tmp_image[:, ::-1, tmp_slice[2]].transpose([1, 0, 2])  # XZ plane

        img_xy = Image.fromarray(image_xy)
        img_xy = img_xy.resize(size=(self.image_width, self.image_height))
        img_yz = Image.fromarray(image_yz)
        img_yz = img_yz.resize(size=(self.image_width, self.image_height))
        img_xz = Image.fromarray(image_xz)
        img_xz = img_xz.resize(size=(self.image_width, self.image_height))

        # Convert the PIL images to Tkinter-compatible images
        img_tk_xy = ImageTk.PhotoImage(image=img_xy)
        img_tk_yz = ImageTk.PhotoImage(image=img_yz)
        img_tk_xz = ImageTk.PhotoImage(image=img_xz)

        self.label_xy.configure(image=img_tk_xy)
        self.label_yz.configure(image=img_tk_yz)
        self.label_xz.configure(image=img_tk_xz)
        # Update the labels with the new images
        self.label_xy_image = img_tk_xy  # Keep a reference to avoid garbage collection
        self.label_yz_image = img_tk_yz  # Keep a reference to avoid garbage collection
        self.label_xz_image = img_tk_xz  # Keep a reference to avoid garbage collection

        self.update_label()
        self.update_rating()

    def next_image(self, event):
        # Increment the index and wrap around if necessary
        self.index = (self.index + 1) % len(self.labels)

        # Update the displayed images
        self.update_images()

    def previous_image(self, event):
        # Decrement the index and wrap around if necessary
        self.index = (self.index - 1) % len(self.labels)

        # Update the displayed images
        self.update_images()

    def save_reference(self, event):
        self.ref_xy_image = self.label_xy_image
        self.ref_yz_image = self.label_yz_image
        self.ref_xz_image = self.label_xz_image

        self.ref_xy.configure(image=self.ref_xy_image)
        self.ref_yz.configure(image=self.ref_yz_image)
        self.ref_xz.configure(image=self.ref_xz_image)

        self.reference_label.configure(text=f"Reference: {self.labels[self.index]}")

    def update_label(self):
        self.subject_label.configure(text=self.labels[self.index])

    def bad_rating(self, event):
        self.ratings[self.labels[self.index]] = "Bad"
        self.update_rating()

    def update_rating(self):
        cur_rating = self.ratings[self.labels[self.index]]

        self.rating_label.configure(
            text=f"Rating:\n{cur_rating}", fg=self.color_dict[cur_rating]
        )

    def neutral_rating(self, event):
        self.ratings[self.labels[self.index]] = "?"
        self.update_rating()

    def good_rating(self, event):
        self.ratings[self.labels[self.index]] = "Good"
        self.update_rating()

    def save_results(self):
        # Format the date and time into a string suitable for a filename

        if self.output is None:
            now = datetime.datetime.now()
            self.output = now.strftime("%Y-%m-%d_%H-%M") + ".json"
        elif os.path.isdir(self.output):
            now = datetime.datetime.now()
            outfile = now.strftime("%Y-%m-%d_%H-%M") + ".json"
            self.output = os.path.join(self.output, outfile)

        with open(self.output, "w", encoding="utf-8") as f:
            json.dump(self.ratings, f, ensure_ascii=False, indent=4)
