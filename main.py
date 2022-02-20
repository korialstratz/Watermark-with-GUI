from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont
import os

FONT_NAME = ("Arial", 12, "bold")
choose_list = ["TEXT", "IMAGE"]
locations = ["RIGHT", "LEFT"]
button_bg = "#20bebe"
button_fg = "white"
wm_text_color = (0, 0, 0)
wm_text_font = "arial.ttf"


class Gui:

    def __init__(self):
        self.window = Tk()
        self.window.title("Watermark")
        self.window.iconbitmap("images/wm.ico")

        self.window.config(padx=30, pady=30)
        self.canvas = Canvas(width=220, height=260)

        # Watermark Functions

        self.first_img = ""
        self.new_name = ""
        self.first_image_width = 0
        self.first_image_height = 0
        self.watermark_img = ""
        self.user_ratio = 0
        self.resize_ratio = 0
        self.new_file_path = ""
        self.position_y = 0
        self.position_x = 0
        self.choose = ""
        self.text = ""
        self.color = wm_text_color
        self.location = ""

        def open_first():
            folder_path = filedialog.askopenfilename(initialdir="/", title="Select a File",
                                                     filetypes=(("Jpeg", "*.jpeg*"), ("all files", "*.*")))
            selected_path = str(folder_path)
            file_name = os.path.basename(folder_path)
            image_name = file_name.split(".")
            new_file_path = selected_path.split("/")
            new_file_path = "".join(new_file_path[:-1])
            self.new_name = f"{image_name[0]}-watermark.{image_name[1]}"
            self.first_img = Image.open(selected_path)
            self.first_image_width, self.first_image_height = self.first_img.size
            return self.first_img, self.new_name, self.first_image_width, self.first_image_height

        def open_second():
            folder_path = filedialog.askopenfilename(initialdir="/", title="Select a File",
                                                     filetypes=(("Jpeg", "*.jpeg*"), ("all files", "*.*")))
            selected_path = str(folder_path)
            self.watermark_img = Image.open(selected_path)
            return self.watermark_img

        def given_ratio(ratio):
            self.resize_ratio = self.first_image_width * (ratio / 100)
            return self.resize_ratio

        def resize_watermark():
            watermark_img_width, watermark_image_height = self.watermark_img.size
            watermark_img_ratio = watermark_image_height / watermark_img_width

            watermark_new_width_ratio = self.resize_ratio / watermark_img_width

            watermark_new_width = watermark_img_width * watermark_new_width_ratio
            watermark_new_height = watermark_new_width * watermark_img_ratio

            self.watermark_img = self.watermark_img.resize((int(watermark_new_width),
                                                            int(watermark_new_height)), Image.ANTIALIAS)

            position(watermark_new_height, watermark_new_width, self.location)

            new_img = self.first_img.copy()
            new_img.paste(self.watermark_img, (int(self.position_x), int(self.position_y)))
            new_img.save(self.new_name)

        def make_text(text):
            new_text_img = self.first_img.copy()
            draw = ImageDraw.Draw(new_text_img)

            font = ImageFont.truetype(wm_text_font, int(self.resize_ratio))
            text_width, text_height = draw.textsize(text, font)

            position(text_height, text_width, self.location)

            draw.text((int(self.position_x), int(self.position_y)), text, self.color, font=font)

            new_text_img.save(self.new_name)

        def position(height, width, location):

            self.position_y = self.first_image_height - height

            if location == "RIGHT":
                self.position_x = self.first_image_width - width
            else:
                self.position_x = 0
            return self.position_y, self.position_x

        def start_watermark():
            given_ratio(self.user_ratio)
            if self.choose == "IMAGE":
                resize_watermark()
            else:
                get_entry()
                make_text(self.watermark_text)

        # Labels

        self.logo = PhotoImage(file="images/watermark.png")
        self.image_label = Label(image=self.logo)
        self.image_label.grid(column=0, row=0, columnspan=2)

        self.ratio_label = Label(text="Ratio", font="Raleway", bg=button_bg, fg=button_fg, height=2, width=5)
        self.ratio_label.grid(column=3, row=1)

        self.bottom_label = Label(text="Watermark your image with logo or text", font=FONT_NAME)
        self.bottom_label.grid(column=1, row=3, columnspan=3, pady=10)

        # Buttons

        self.open_first_button = Button(text="Image to Watermark", command=open_first, font="Raleway",
                                        bg=button_bg, fg=button_fg, height=2, width=20)
        self.open_first_button.grid(column=0, row=1, pady=10)

        self.open_watermark_button = Button(text="Watermark Image", command=open_second, font="Raleway",
                                            bg=button_bg, fg=button_fg, height=2, width=20)
        self.open_watermark_button.grid(column=0, row=2, sticky="n")

        self.apply_button = Button(text="Apply Watermark", command=start_watermark, font="Raleway",
                                   bg=button_bg, fg=button_fg, height=2, width=20)
        self.apply_button.grid(column=0, row=3, sticky="n")

        # Listbox for image or text
        def listbox_choose(event):
            # Gets current selection from listbox
            self.choose = self.listbox.get(self.listbox.curselection())
            return self.choose

        # exportselection = 0 to use multiple listbox
        self.listbox = Listbox(height=2, exportselection=0, font="Raleway", bg=button_bg, fg=button_fg, width=11)
        for item in choose_list:
            self.listbox.insert(choose_list.index(item), item)
        self.listbox.bind("<<ListboxSelect>>", listbox_choose)
        self.listbox.grid(column=1, row=1, padx=10, pady=10)

        # Listbox for location
        def listbox_location(event_2):
            # Gets current selection from listbox
            self.location = self.listbox_2.get(self.listbox_2.curselection())
            return self.location

        self.listbox_2 = Listbox(height=2, exportselection=0, font="Raleway", bg=button_bg, fg=button_fg, width=11)
        for item in locations:
            self.listbox_2.insert(locations.index(item), item)
        self.listbox_2.bind("<<ListboxSelect>>", listbox_location)
        self.listbox_2.grid(column=2, row=1, sticky="e", padx=10)

        # Scale
        def scale_used(value):
            self.user_ratio = value
            self.user_ratio = int(self.user_ratio)
            return self.user_ratio

        self.scale = Scale(from_=0, to=100, command=scale_used, font="Raleway", bg=button_bg, fg=button_fg)
        self.scale.grid(column=3, row=2, pady=10)

        # Entry
        self.entry = Entry(width=25, font="Raleway", bg=button_bg, fg=button_fg)
        # Add some text to begin with
        self.entry.insert(END, string="Enter your text")
        self.entry.grid(column=1, row=2, columnspan=2, padx=10, pady=10, sticky="n")

        # Gets text in entry
        def get_entry():
            self.watermark_text = self.entry.get()
            return self.watermark_text

        self.window.mainloop()


if __name__ == '__main__':
    Gui()
