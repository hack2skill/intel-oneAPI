import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, Frame, filedialog, Label, DISABLED, ACTIVE
from PIL import Image, ImageTk, ImageGrab
import configparser
import json
import pybboxes as pbx
import geocoder
import time
import cv2
from datetime import datetime


class CreateToolTip(object):

    def __init__(self, widget, text='widget info'):
        self.waittime = 500
        self.wraplength = 180
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                         background="#ffffff", relief='solid', borderwidth=1,
                         wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


focus_area = []


class MousePositionTracker(tk.Frame):
    """ Tkinter Canvas mouse position widget. """

    def __init__(self, canvas):
        self.canvas = canvas
        self.canv_width = self.canvas.cget('width')
        self.canv_height = self.canvas.cget('height')
        self.reset()

        # Create canvas cross-hair lines.
        xhair_opts = dict(dash=(3, 2), fill='white', state=tk.HIDDEN)
        self.lines = (self.canvas.create_line(0, 0, 0, self.canv_height, **xhair_opts),
                      self.canvas.create_line(0, 0, self.canv_width, 0, **xhair_opts))

    def cur_selection(self):
        return (self.start, self.end)

    def begin(self, event):
        self.hide()
        self.start = (event.x, event.y)  # Remember position (no drawing).

    def update(self, event):
        self.end = (event.x, event.y)
        self._update(event)
        self._command(self.start, (event.x, event.y))  # User callback.

    def _update(self, event):
        # Update cross-hair lines.
        self.canvas.coords(self.lines[0], event.x, 0, event.x, self.canv_height)
        self.canvas.coords(self.lines[1], 0, event.y, self.canv_width, event.y)
        self.show()

    def reset(self):
        self.start = self.end = None

    def hide(self):
        self.canvas.itemconfigure(self.lines[0], state=tk.HIDDEN)
        self.canvas.itemconfigure(self.lines[1], state=tk.HIDDEN)

    def show(self):
        self.canvas.itemconfigure(self.lines[0], state=tk.NORMAL)
        self.canvas.itemconfigure(self.lines[1], state=tk.NORMAL)

    def autodraw(self, command=lambda *args: None):
        """Setup automatic drawing; supports command option"""
        self.reset()
        self._command = command
        self.canvas.bind("<Button-1>", self.begin)
        self.canvas.bind("<B1-Motion>", self.update)
        self.canvas.bind("<ButtonRelease-1>", self.quit)

    def quit(self, event):
        self.hide()  # Hide cross-hairs.
        self.reset()


class SelectionObject:
    """ Widget to display a rectangular area on given canvas defined by two points
        representing its diagonal.
    """

    def __init__(self, canvas, select_opts):
        # Create attributes needed to display selection.
        self.canvas = canvas
        self.select_opts1 = select_opts
        self.width = self.canvas.cget('width')
        self.height = self.canvas.cget('height')

        # Options for areas outside rectanglar selection.
        select_opts1 = self.select_opts1.copy()  # Avoid modifying passed argument.
        select_opts1.update(state=tk.HIDDEN)  # Hide initially.
        # Separate options for area inside rectanglar selection.
        select_opts2 = dict(dash=(2, 2), fill='', outline='white', state=tk.HIDDEN)

        # Initial extrema of inner and outer rectangles.
        imin_x, imin_y, imax_x, imax_y = 0, 0, 1, 1
        omin_x, omin_y, omax_x, omax_y = 0, 0, self.width, self.height

        self.rects = (
            # Area *outside* selection (inner) rectangle.
            self.canvas.create_rectangle(omin_x, omin_y, omax_x, imin_y, **select_opts1),
            self.canvas.create_rectangle(omin_x, imin_y, imin_x, imax_y, **select_opts1),
            self.canvas.create_rectangle(imax_x, imin_y, omax_x, imax_y, **select_opts1),
            self.canvas.create_rectangle(omin_x, imax_y, omax_x, omax_y, **select_opts1),
            # Inner rectangle.
            self.canvas.create_rectangle(imin_x, imin_y, imax_x, imax_y, **select_opts2)
        )

    def update(self, start, end):
        # Current extrema of inner and outer rectangles.
        imin_x, imin_y, imax_x, imax_y = self._get_coords(start, end)
        omin_x, omin_y, omax_x, omax_y = 0, 0, self.width, self.height

        # Update coords of all rectangles based on these extrema.
        self.canvas.coords(self.rects[0], omin_x, omin_y, omax_x, imin_y),
        self.canvas.coords(self.rects[1], omin_x, imin_y, imin_x, imax_y),
        self.canvas.coords(self.rects[2], imax_x, imin_y, omax_x, imax_y),
        self.canvas.coords(self.rects[3], omin_x, imax_y, omax_x, omax_y),
        self.canvas.coords(self.rects[4], imin_x, imin_y, imax_x, imax_y),

        for rect in self.rects:  # Make sure all are now visible.
            self.canvas.itemconfigure(rect, state=tk.NORMAL)

    def _get_coords(self, start, end):
        """ Determine coords of a polygon defined by the start and
            end points one of the diagonals of a rectangular area.
        """

        focus_area = [min((start[0], end[0])), min((start[1], end[1])), max((start[0], end[0])),
                      max((start[1], end[1]))]

        return (focus_area)

    def hide(self):
        for rect in self.rects:
            self.canvas.itemconfigure(rect, state=tk.HIDDEN)


version = '1.0.1'


def main():
    def loading():
        rootx = tk.Tk()
        rootx.iconbitmap(default='Data/Images/icons/favicon.ico')
        rootx.image = tk.PhotoImage(file='Data/Images/Background/load.gif')
        labelx = tk.Label(rootx, image=rootx.image, bg='white')
        rootx.overrideredirect(True)
        rootx.geometry("+600+100")
        rootx.wm_attributes("-topmost", True)
        rootx.wm_attributes("-disabled", True)
        rootx.wm_attributes("-transparentcolor", "white")
        labelx.pack()
        labelx.after(500, lambda: labelx.destroy())
        rootx.after(500, lambda: rootx.destroy())  # Destroy the widget after 0.5 seconds
        labelx.mainloop()

    for i in range(0, 1):
        loading()

    def display():

        class Store_DATA_IN_INI:

            def __init__(self, win):

                load = cv2.imread('Data/Images/Background/background.jpg', 1)
                cv2imagex1 = cv2.cvtColor(load, cv2.COLOR_BGR2RGBA)
                load = Image.fromarray(cv2imagex1)
                regx = tk.Tk()
                load = load.resize((int(regx.winfo_screenwidth()), int(regx.winfo_screenheight())), Image.LANCZOS)

                render = ImageTk.PhotoImage(load)
                img = tk.Label(image=render)
                img.image = render
                img.place(x=-1, y=0)

                load = cv2.imread('Data/Images/Background/logo.png', 1)
                cv2imagex1 = cv2.cvtColor(load, cv2.COLOR_BGR2RGBA)
                load = Image.fromarray(cv2imagex1)
                load = load.resize((int(250), int(160)), Image.LANCZOS)
                render = ImageTk.PhotoImage(load)
                img = tk.Label(image=render)
                img.image = render
                img.place(x=1665, y=0)

                self.b0 = tk.Button(win,
                                    bg='#f7421e',
                                    fg='#b7f731',
                                    relief='flat',
                                    width=20, command=self.quit)
                self.b0.place(x=0, y=0, width=150, height=150)

                self.b0b = tk.Button(win,
                                     bg='#33ff00',
                                     fg='#b7f731',
                                     relief='flat',
                                     width=100, command=self.settings)
                self.b0b.place(x=1770, y=950, width=150, height=150)

                self.b1 = ttk.Button(win, text='Live Dash Cam with Segmentation', width=20, command=self.pot_holes)
                self.b1.place(x=90, y=470, width=300, height=100)

                self.b2 = ttk.Button(win, text='Uploaded Data Viewer', width=20, command=self.data_viewer)
                self.b2.place(x=300, y=780, width=300, height=100)

                self.b3 = ttk.Button(win, text='Live Dash Cam', width=20, command=self.dash_cam)
                self.b3.place(x=1400, y=220, width=300, height=100)

                self.b4 = ttk.Button(win, text='Detect Picture', width=20, command=self.label_picture)
                self.b4.place(x=1480, y=530, width=300, height=100)

                regx.destroy()

            def settings(self):

                class TOKENS:

                    def __init__(self, tokens):

                        config = configparser.ConfigParser()
                        config.read('Data/Keys/config.ini')
                        config_token = config.items('TOKEN')
                        TOKEN = str(config_token[0][1])
                        UP_URL = str(config_token[1][1])

                        self.lbl = tk.Label(tokens, text="TOKEN", font=("Helvetica", 30, 'bold'), bg='white')
                        self.lbl.place(x=60, y=70)

                        self.txtfld1 = ttk.Combobox(tokens, font=("Helvetica", 30, 'bold'))
                        self.txtfld1.place(x=220, y=70, width=550)
                        self.txtfld1.set(TOKEN)

                        self.lb2 = tk.Label(tokens, text="USER", font=("Helvetica", 30, 'bold'), bg='white')
                        self.lb2.place(x=60, y=170)

                        self.txtfld2 = ttk.Combobox(tokens, font=("Helvetica", 30, 'bold'))
                        self.txtfld2.place(x=220, y=170, width=550)
                        self.txtfld2.set(UP_URL)

                        self.btn = ttk.Button(tokens, text="UPDATE", width=20, command=self.token_validate)
                        self.btn.place(x=500, y=250, width=270, height=50)

                    def token_validate(self):
                        if (str(self.txtfld1.get()) != "") and (str(self.txtfld2.get()) != ""):

                            config = configparser.ConfigParser()
                            config.write('Data/Keys/config.ini')

                            file = open('Data/Keys/config.ini', "w+")

                            config.add_section('TOKEN')
                            config.set('TOKEN', 'TOKEN', str(self.txtfld1.get()))
                            config.set('TOKEN', 'UP_URL', str(self.txtfld2.get()))

                            config.write(file)
                            file.close()

                            tk.messagebox.showinfo("Success", "Updated Successfully")

                            tokens_user_login.destroy()

                        else:
                            tk.messagebox.showerror("Error", "EMPTY VALUES")

                    @staticmethod
                    def quit():
                        tokens_user_login.destroy()

                tokens_user_login = tk.Tk()
                tokens_user_login.config(background='white')
                tokens_user_login.attributes('-alpha', 0.9)

                TOKENS(tokens_user_login)
                tokens_user_login.iconbitmap(default='Data/Images/icons/favicon.ico')
                tokens_user_login.title('oneAPI_ODAV  Car Dashboard Settings ' + version)
                tokens_user_login.geometry("850x350")
                tokens_user_login.mainloop()

            @staticmethod
            def quit():
                window_user_login1.destroy()
                exit(0)

            def pot_holes(self):
                import torch
                with torch.no_grad():
                    from ENGINES import AI_POTHOLES_DETECTION
                    AI_POTHOLES_DETECTION.AI_POTHOLES_DETECTION(source="TEST_VIDEO/testx.mp4",
                                                                model_weights="Model/yolov7.pt")
                    # window_user_login1.destroy()
                # second(user_key=user_key, job="HOSTEL ENVIRONMENT")

            def data_viewer(self):
                window_user_login1.destroy()
                data_viewer()

            def dash_cam(self):
                import torch
                with torch.no_grad():
                    from ENGINES import AI_DASH_CAM
                    AI_DASH_CAM.AI_DASH_CAM(source="TEST_VIDEO/testx.mp4",
                                            model_weights="Model/yolov7.pt")
                # window_user_login1.destroy()
                # second(user_key=user_key, job="BUS ENVIRONMENT")

            def label_picture(self):
                filename = filedialog.askopenfilename(initialdir="/",
                                                      title="Select a image File",
                                                      filetypes=(("Image files",
                                                                  "*.jpg"),
                                                                 ("Image files",
                                                                  "*.jpeg*"),
                                                                 ("Image files",
                                                                  "*.png*")
                                                                 ))
                import torch
                from ENGINES import AI_DASH_CAM_IMAGE
                AI_DASH_CAM_IMAGE.AI_DASH_CAM_IMAGE(filename, model_weights="Model/yolov7.pt")
                # second(user_key=user_key, job="EXAM ENVIRONMENT")

            @staticmethod
            def start(self):
                window_user_login1.destroy()
                # second(user_key=user_key, job="START ENVIRONMENT")

        window_user_login1 = tk.Tk()
        window_user_login1.config(background='#EFEFEF')
        window_user_login1.attributes('-fullscreen', True)

        Store_DATA_IN_INI(window_user_login1)
        window_user_login1.iconbitmap(default='Data/Images/icons/favicon.ico')
        window_user_login1.title('oneAPI_ADAV')
        window_user_login1.mainloop()

    def data_viewer():

        class View_Image(tk.Frame):

            # Default selection object options.
            SELECT_OPTS = dict(dash=(2, 2), stipple='gray25', fill='red',
                               outline='')

            def __init__(self, win, *args, **kwargs):
                super().__init__(win, *args, **kwargs)

                self.label_class = {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus',
                                    6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light',
                                    10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird',
                                    15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow',
                                    20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack',
                                    25: 'umbrella',
                                    26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee',
                                    30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat',
                                    35: 'baseball glove', 36: 'skateboard', 37: 'surfboard',
                                    38: 'tennis racket', 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork',
                                    43: 'knife',
                                    44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple',
                                    48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog',
                                    53: 'pizza',
                                    54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch',
                                    58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv',
                                    63: 'laptop',
                                    64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone',
                                    68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator',
                                    73: 'book',
                                    74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear',
                                    78: 'hair drier', 79: 'toothbrush'}

                self.image_class = {'person': 0, 'bicycle': 1, 'car': 2, 'motorcycle': 3, 'airplane': 4, 'bus': 5,
                                    'train': 6, 'truck': 7, 'boat': 8, 'traffic light': 9,
                                    'fire hydrant': 10, 'stop sign': 11, 'parking meter': 12, 'bench': 13, 'bird': 14,
                                    'cat': 15, 'dog': 16, 'horse': 17, 'sheep': 18, 'cow': 19,
                                    'elephant': 20, 'bear': 21, 'zebra': 22, 'giraffe': 23, 'backpack': 24,
                                    'umbrella': 25,
                                    'handbag': 26, 'tie': 27, 'suitcase': 28, 'frisbee': 29,
                                    'skis': 30, 'snowboard': 31, 'sports ball': 32, 'kite': 33, 'baseball bat': 34,
                                    'baseball glove': 35, 'skateboard': 36, 'surfboard': 37,
                                    'tennis racket': 38, 'bottle': 39, 'wine glass': 40, 'cup': 41, 'fork': 42,
                                    'knife': 43,
                                    'spoon': 44, 'bowl': 45, 'banana': 46, 'apple': 47,
                                    'sandwich': 48, 'orange': 49, 'broccoli': 50, 'carrot': 51, 'hot dog': 52,
                                    'pizza': 53,
                                    'donut': 54, 'cake': 55, 'chair': 56, 'couch': 57,
                                    'potted plant': 58, 'bed': 59, 'dining table': 60, 'toilet': 61, 'tv': 62,
                                    'laptop': 63,
                                    'mouse': 64, 'remote': 65, 'keyboard': 66, 'cell phone': 67,
                                    'microwave': 68, 'oven': 69, 'toaster': 70, 'sink': 71, 'refrigerator': 72,
                                    'book': 73,
                                    'clock': 74, 'vase': 75, 'scissors': 76, 'teddy bear': 77,
                                    'hair drier': 78, 'toothbrush': 79}

                selected_values = ["", "", "", "", "", "", "", "", "", "", ""]

                def on_drag(start, end, **kwarg):  # Must accept these arguments.
                    self.selection_obj.update(start, end)
                    focus_area = self.selection_obj._get_coords(start, end)

                    print(focus_area)

                    x1, y1, x2, y2 = pbx.convert_bbox(focus_area, from_type="voc", to_type="yolo",
                                                      image_size=(665, 600))

                    print(x1, y1, x2, y2)

                    if x1 != 0.5 and y1 != 0.5 and x2 != 1.0 and y2 != 1.0:
                        self.txtfld3.set(str(x1))
                        self.txtfld4.set(str(y1))
                        self.txtfld5.set(str(x2))
                        self.txtfld6.set(str(y2))

                def open_image_file():
                    filename = filedialog.askopenfilename(initialdir="/",
                                                          title="Select a image File",
                                                          filetypes=(("Image files",
                                                                      "*.jpg"),
                                                                     ("Image files",
                                                                      "*.jpeg*"),
                                                                     ("Image files",
                                                                      "*.png*")
                                                                     ))
                    new_camera(filename)

                def new_camera(path=0):

                    vid = cv2.VideoCapture(path)

                    # Declare the width and height in variables
                    wi, hi = 665, 600

                    # Set the width and height
                    vid.set(cv2.CAP_PROP_FRAME_WIDTH, wi)
                    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, hi)

                    _, frame = vid.read()

                    # Convert image from one color space to other
                    opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

                    # Capture the latest frame and transform to image
                    captured_image = Image.fromarray(opencv_image).resize((665, 600), Image.LANCZOS)

                    # Convert captured image to photoimage
                    photo_image = ImageTk.PhotoImage(image=captured_image)

                    self.canvas = tk.Canvas(win, width=wi, height=hi,
                                            scrollregion=(0, 0, 500, 500))
                    self.canvas.place(x=1250, y=150)

                    self.canvas.create_image(0, 0, image=photo_image, anchor=tk.NW)
                    self.canvas.img = photo_image  # Keep reference.

                    # Create selection object to show current selection boundaries.
                    self.selection_obj = SelectionObject(self.canvas, self.SELECT_OPTS)

                    # Callback function to update it given two points of its diagonal.

                    # Create mouse position tracker that uses the function.
                    self.posn_tracker = MousePositionTracker(self.canvas)
                    self.posn_tracker.autodraw(command=on_drag)  # Enable callbacks.

                    latitude, longitude = geocoder.ip('me').latlng

                    config = configparser.ConfigParser()
                    config.read('Data/Keys/config.ini')
                    config_token = config.items('TOKEN')
                    UP_URL = str(config_token[1][1])

                    self.txtfld1.set(UP_URL)
                    self.txtfld2.set("")
                    self.txtfld3.set("")
                    self.txtfld4.set("")
                    self.txtfld5.set("")
                    self.txtfld6.set("")
                    self.txtfld7.set(latitude)
                    self.txtfld8.set(longitude)

                    self.btn_submit.config(state=ACTIVE)
                    vid.release()

                def selectItem(a):
                    curItem = self.tree.focus()

                    selected_values = (self.tree.item(curItem)['values'])

                    path = selected_values[2]

                    if path == "":
                        path = "Data/Images/Background/no_image.jpg"

                    imgx = ImageTk.PhotoImage(Image.open(path))

                    width = imgx.width() / 665
                    height = imgx.height() / 600

                    wi, hi = imgx.width(), imgx.height()

                    img = ImageTk.PhotoImage(Image.open(path).resize((665, 600), Image.LANCZOS))

                    self.canvas = tk.Canvas(win, width=img.width(), height=img.height(),
                                            scrollregion=(0, 0, 500, 500))
                    self.canvas.place(x=1250, y=150)

                    self.canvas.create_image(0, 0, image=img, anchor=tk.NW)
                    self.canvas.img = img  # Keep reference.

                    # Create selection object to show current selection boundaries.
                    self.selection_obj = SelectionObject(self.canvas, self.SELECT_OPTS)

                    # Callback function to update it given two points of its diagonal.

                    # Create mouse position tracker that uses the function.
                    self.posn_tracker = MousePositionTracker(self.canvas)
                    self.posn_tracker.autodraw(command=on_drag)  # Enable callbacks.

                    center_X = (float(selected_values[3]) * wi) / width
                    center_y = (float(selected_values[4]) * hi) / height
                    widthx = (float(selected_values[5]) * wi) / width
                    heightx = (float(selected_values[6]) * hi) / height

                    x = int(center_X - (widthx / 2))
                    y = int(center_y - (heightx / 2))

                    on_drag((int(x), int(y)), (x + int(widthx), int(y + heightx)))

                    self.txtfld1.set(selected_values[1])
                    self.txtfld2.set(selected_values[9])
                    self.txtfld3.set(selected_values[3])
                    self.txtfld4.set(selected_values[4])
                    self.txtfld5.set(selected_values[5])
                    self.txtfld6.set(selected_values[6])
                    self.txtfld7.set(selected_values[7])
                    self.txtfld8.set(selected_values[8])

                    if selected_values[11] == "Yes":
                        self.btn_submit.config(state=DISABLED)
                    else:
                        self.btn_submit.config(state=ACTIVE)

                def validate():
                    try:
                        on_drag((int(0), int(0)), (665, 600))
                        time.sleep(1)
                        now = datetime.now()
                        filename = "Data/Saved_Images/" + str(now.strftime("%Y%m%d%H%M%S") + str(".jpg"))
                        ImageGrab.grab(bbox=(
                            self.canvas.winfo_rootx(),
                            self.canvas.winfo_rooty(),
                            self.canvas.winfo_rootx() + self.canvas.winfo_width(),
                            self.canvas.winfo_rooty() + self.canvas.winfo_height()
                        )).save(filename)

                        json_data = {
                            "userid": str(self.txtfld1.get()),
                            "image_url": filename,
                            "w_cord": float(self.txtfld3.get()),
                            "x_cord": float(self.txtfld4.get()),
                            "y_cord": float(self.txtfld5.get()),
                            "z_cord": float(self.txtfld6.get()),
                            "latitude": float(self.txtfld7.get()),
                            "longitude": float(self.txtfld8.get()),
                            "class_of_image": self.image_class[str(self.txtfld2.get())],
                            "auto": "No",
                            "uploaded": "No"
                        }

                        print(json_data)

                        with open('Data/Data/sample.json', 'r+') as openfile:
                            # Reading from json file
                            json_object = json.load(openfile)
                            json_object["data"].append(json_data)
                            openfile.seek(0)
                            json.dump(json_object, openfile, indent=4)

                        print(json_data)

                        messagebox.showinfo("Successfully", "The data saved into Json Data successfully")
                        load_tree()
                    except Exception:
                        print(Exception)
                        messagebox.showerror("Operation failed", "The data cannot be saved. Entered data invalid")

                def load_tree():

                    self.temp_values = []

                    with open('Data/Data/sample.json', 'r') as openfile:
                        # Reading from json file
                        json_object = json.load(openfile)
                        for each in json_object["data"]:
                            self.temp_values.append([each["userid"], each["image_url"], each["w_cord"], each["x_cord"],
                                                     each["y_cord"], each["z_cord"], each["latitude"],
                                                     each["longitude"],
                                                     each["class_of_image"], each["auto"], each["uploaded"]])

                    self.frame = Frame(win)
                    self.frame.place(x=20, y=755)

                    self.tree = ttk.Treeview(self.frame, columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), height=14,
                                             show="headings")
                    self.tree.pack(side='left')
                    self.tree.bind('<ButtonRelease-1>', selectItem)

                    self.val = ["serial No", "User Id", "Image Url", "W Coordinate", "X Coordinate", "Y Coordinate",
                                "Z Coordinate", "Latitude", "Longitude", "Class Of Image", "Auto", "Uploaded"]

                    for ii in range(1, len(self.val) + 1):
                        self.tree.heading(ii, text=self.val[ii - 1])

                    for ii in range(1, len(self.val) + 1):
                        self.tree.column(ii, width=156, anchor='center')

                    self.scroll1 = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
                    self.scroll1.pack(side='right', fill='y')

                    for i in range(len(self.temp_values) - 1, -1, -1):
                        if str(self.temp_values[i][10]) == "Yes":
                            self.tree.insert('', 'end', values=(str(i),
                                                                str(self.temp_values[i][0]),
                                                                str(self.temp_values[i][1]),
                                                                str(self.temp_values[i][2])
                                                                , str(self.temp_values[i][3]),
                                                                str(self.temp_values[i][4]),
                                                                str(self.temp_values[i][5]),
                                                                str(self.temp_values[i][6]),
                                                                str(self.temp_values[i][7]),
                                                                str(self.label_class[self.temp_values[i][8]]),
                                                                str(self.temp_values[i][9]),
                                                                str(self.temp_values[i][10])),
                                             tags=('odd',))
                        else:
                            self.tree.insert('', 'end', values=(str(i),
                                                                str(self.temp_values[i][0]),
                                                                str(self.temp_values[i][1]),
                                                                str(self.temp_values[i][2])
                                                                , str(self.temp_values[i][3]),
                                                                str(self.temp_values[i][4]),
                                                                str(self.temp_values[i][5]),
                                                                str(self.temp_values[i][6]),
                                                                str(self.temp_values[i][7]),
                                                                str(self.label_class[self.temp_values[i][8]]),
                                                                str(self.temp_values[i][9]),
                                                                str(self.temp_values[i][10])),
                                             tags=('even',))

                    self.tree.tag_configure('odd', background='#CCFF99')
                    self.tree.tag_configure('even', background='#FFFF99')

                load = cv2.imread('Data/Images/Background/background_2.jpg', 1)
                cv2imagex1 = cv2.cvtColor(load, cv2.COLOR_BGR2RGBA)
                load = Image.fromarray(cv2imagex1)
                load = load.resize((int(1920), int(1080)), Image.LANCZOS)
                render = ImageTk.PhotoImage(load)
                img = tk.Label(image=render)
                img.image = render
                img.place(x=0, y=0)

                load = cv2.imread('Data/Images/Background/logo.png', 1)
                cv2imagex1 = cv2.cvtColor(load, cv2.COLOR_BGR2RGBA)
                load = Image.fromarray(cv2imagex1)
                load = load.resize((int(250), int(160)), Image.LANCZOS)
                render = ImageTk.PhotoImage(load)
                img = tk.Label(image=render)
                img.image = render
                img.place(x=1515, y=0)

                path = "Data/Images/Background/no_image.jpg"
                imgx = ImageTk.PhotoImage(Image.open(path))

                width = int(imgx.width() // 665)
                height = int(imgx.height() // 600)

                img = ImageTk.PhotoImage(Image.open(path).resize((665, 600), Image.LANCZOS))

                self.canvas = tk.Canvas(win, width=img.width(), height=img.height(),
                                        scrollregion=(0, 0, 500, 500))
                self.canvas.place(x=1250, y=150)

                self.canvas.create_image(0, 0, image=img, anchor=tk.NW)
                self.canvas.img = img  # Keep reference.

                # LABEL AND TEXT BOX TO ENTER DETAILS OF ALL ELEMENTS OF A STATION
                self.lb_title = Label(win, text="Image Data Captured",
                                      font=("Ariel", 40, "bold"), bg='#F7F7F9')
                self.lb_title.place(x=420, y=200)

                self.lb1 = Label(win, text="User Id", font=("Helvetica", 20), bg='#F7F7F9')
                self.lb1.place(x=60, y=350)

                self.txtfld1 = ttk.Combobox(win, font=("Helvetica", 20), )
                self.txtfld1.place(x=300, y=350)
                self.txtfld1.set(selected_values[1])
                self.txtfld1.configure(state=DISABLED)

                self.lb2 = Label(win, text="Image Class", fg='black', font=("Helvetica", 20), bg='#F7F7F9')
                self.lb2.place(x=650, y=350)

                self.txtfld2 = ttk.Combobox(win, font=("Helvetica", 20),
                                            values=['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
                                                    'train', 'truck', 'boat', 'traffic light',
                                                    'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
                                                    'cat', 'dog', 'horse', 'sheep', 'cow',
                                                    'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella',
                                                    'handbag', 'tie', 'suitcase', 'frisbee',
                                                    'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat',
                                                    'baseball glove', 'skateboard', 'surfboard',
                                                    'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife',
                                                    'spoon', 'bowl', 'banana', 'apple',
                                                    'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
                                                    'donut', 'cake', 'chair', 'couch',
                                                    'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop',
                                                    'mouse', 'remote', 'keyboard', 'cell phone',
                                                    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book',
                                                    'clock', 'vase', 'scissors', 'teddy bear',
                                                    'hair drier', 'toothbrush'])
                self.txtfld2.place(x=890, y=350)
                self.txtfld2.set(selected_values[9])

                self.lb3 = Label(win, text="W Coordinate", fg='black', font=("Helvetica", 20), bg='#F7F7F9')
                self.lb3.place(x=60, y=425)

                self.txtfld3 = ttk.Combobox(win, font=("Helvetica", 20))
                self.txtfld3.place(x=300, y=425)
                self.txtfld3.set(selected_values[3])
                self.txtfld3.config(state=DISABLED)

                self.lb4 = Label(win, text="X Coordinate", fg='black', font=("Helvetica", 20), bg='#F7F7F9')
                self.lb4.place(x=650, y=425)

                self.txtfld4 = ttk.Combobox(win, font=("Helvetica", 20))
                self.txtfld4.place(x=890, y=425)
                self.txtfld4.set(selected_values[4])
                self.txtfld4.config(state=DISABLED)

                self.lb5 = Label(win, text="Y Coordinate", fg='black', font=("Helvetica", 20), bg='#F7F7F9')
                self.lb5.place(x=60, y=500)

                self.txtfld5 = ttk.Combobox(win, font=("Helvetica", 20))
                self.txtfld5.place(x=300, y=500)
                self.txtfld5.set(selected_values[5])
                self.txtfld5.config(state=DISABLED)

                self.lb6 = Label(win, text="Z Coordinate", fg='black', font=("Helvetica", 20), bg='#F7F7F9')
                self.lb6.place(x=650, y=500)

                self.txtfld6 = ttk.Combobox(win, font=("Helvetica", 20))
                self.txtfld6.place(x=890, y=500)
                self.txtfld6.set(selected_values[6])
                self.txtfld6.config(state=DISABLED)

                self.lb7 = Label(win, text="Latitude", fg='black', font=("Helvetica", 20), bg='#F7F7F9')
                self.lb7.place(x=60, y=575)

                self.txtfld7 = ttk.Combobox(win, font=("Helvetica", 20))
                self.txtfld7.place(x=300, y=575)
                self.txtfld7.set(selected_values[7])
                self.txtfld7.config(state=DISABLED)

                self.lb8 = Label(win, text="Longitude", fg='black', font=("Helvetica", 20), bg='#F7F7F9')
                self.lb8.place(x=650, y=575)

                self.txtfld8 = ttk.Combobox(win, font=("Helvetica", 20))
                self.txtfld8.place(x=890, y=575)
                self.txtfld8.set(selected_values[8])
                self.txtfld8.config(state=DISABLED)

                load_tree()

                self.btn_submit = ttk.Button(win, text="SUBMIT", command=validate)
                self.btn_submit.place(x=540, y=660, width=250, height=60)

                s = ttk.Style()
                s.configure('my.TButton', font=('Aerial', 18, 'bold'))

                self.btn_edit_images = ttk.Button(win, text="IMAGES", style='my.TButton', width=20,
                                                  command=open_image_file)
                self.btn_edit_images.place(x=150, y=0, width=300, height=150)

                self.btn_new_camera = ttk.Button(win, text="CAMERA", style='my.TButton', width=20, command=new_camera)
                self.btn_new_camera.place(x=450, y=0, width=300, height=150)

                self.b0 = tk.Button(win,
                                    bg='#33ff00',
                                    fg='#b7f731',
                                    relief='flat',
                                    width=20, command=self.back)
                self.b0.place(x=0, y=0, width=150, height=150)

                self.b0r = tk.Button(win,
                                     bg='#f7421e',
                                     fg='#b7f731',
                                     relief='flat',
                                     width=20, command=self.quit)
                self.b0r.place(x=1770, y=0, width=150, height=150)

            @staticmethod
            def quit():
                window_user_login3.destroy()
                exit(0)

            @staticmethod
            def back():
                window_user_login3.destroy()
                display()

        window_user_login3 = tk.Tk()
        window_user_login3.config(background='#EFEFEF')
        window_user_login3.attributes('-fullscreen', True)

        View_Image(window_user_login3)
        window_user_login3.iconbitmap(default='Data/Images/icons/favicon.ico')
        window_user_login3.title('oneAPI_ODAV')
        window_user_login3.mainloop()

    display()


if __name__ == '__main__':
    main()
