from tkinter import *
from PIL import ImageTk, Image, ImageDraw, ImageFont
from tkinter import filedialog


def setup():
    global b_width, b_height, img_size_scale, img, img_to_show, transparent, \
        left_bottom, left_upper, right_bottom, right_upper, img_watermark_save, text_watermark_save
    b_width = b_height = img_size_scale = 0  # img width height before resizing
    img = img_to_show = transparent = None
    left_upper = left_bottom = right_bottom = right_upper = img_watermark_save = text_watermark_save = False

setup()
FONT_SIZE = 30
font = ImageFont.truetype("arial.ttf", FONT_SIZE)


def open_img():
    global img, b_width, b_height, img_to_show, img_size_scale, panel
    filename = openfilename()
    if filename == "":
        return None
    img = Image.open(filename).convert("RGBA")
    b_width, b_height = img.size
    if b_width > 480 and b_height > 360:
        img_width_scale = round(b_width/480)
        img_height_scale = round(b_height/360)
        img_size_scale = round((img_width_scale + img_height_scale) / 2)
    else:
        img_width_scale = round(b_width / 480, 1)
        img_height_scale = round(b_height / 360, 1)
        img_size_scale = round((img_width_scale+img_height_scale)/2, 1)
    img_to_show = img.resize((480, 360))
    img_b = ImageTk.PhotoImage(img_to_show)
    panel = Label(image=img_b)
    panel.img = img_b
    panel.place(x=300, y=200)


def add_text_watermark():
    global img, img_to_show, font, img_size_scale, text_watermark_save, panel
    if img is None:
        print_error(3)
        return None
    draw = ImageDraw.Draw(img)
    draw_to_show = ImageDraw.Draw(img_to_show)
    input = retrieve_input()
    measure["text"] = input
    measure.update_idletasks()  # calculate the width
    width = measure.winfo_width()  # get the width
    margin_h = 480 - width

    font_size_scaled = int(FONT_SIZE * img_size_scale)
    font_scaled_label = ("arial.ttf", round(font_size_scaled * 0.75))
    font_scaled = ImageFont.truetype("arial.ttf", font_size_scaled)

    label_scaled["font"] = font_scaled_label
    label_scaled["text"] = input
    label_scaled.update_idletasks()
    width_scaled = label_scaled.winfo_width()
    margin_h_scaled = b_width - width_scaled
    margin_v_scaled = b_height - 30 * img_size_scale
    if input != "":
        if left_upper is True:
            draw_to_show.text((0, 0), input, (255,0,0), font=font)
            draw.text((0, 0), input, (255,0,0), font=font_scaled)
        elif left_bottom is True:
            draw_to_show.text((0, 330), input, (255, 0, 0), font=font)
            draw.text((0, margin_v_scaled), input, (255, 0, 0), font=font_scaled)
        elif right_bottom is True:
            draw_to_show.text((margin_h, 330), input, (255, 0, 0), font=font)
            draw.text((margin_h_scaled, margin_v_scaled), input, (255,0,0), font=font_scaled)
        elif right_upper is True:
            draw_to_show.text((margin_h, 0), input, (255, 0, 0), font=font)
            draw.text((margin_h_scaled, 0), input, (255, 0, 0), font=font_scaled)
        else:
            print_error(2)
            return None
        modified_img = ImageTk.PhotoImage(img_to_show)
        panel = Label(image=modified_img)
        panel.img = modified_img
        panel.place(x=300, y=200)
        text_watermark_save = True


def add_img_watermark():
    global img, img_to_show, b_width, b_height, img_watermark_save, transparent, panel
    if img is None:
        print_error(3)
        return None
    filename_watermark = openfilename()
    if filename_watermark == "":
        return None
    width, height = img_to_show.size
    watermark = Image.open(filename_watermark).convert("RGBA")
    watermark = watermark.resize((50*img_size_scale, 50*img_size_scale))
    watermark_to_show = watermark.resize((50, 50))
    transparent = Image.new('RGBA', (b_width, b_height), (0, 0, 0, 0))
    transparent.paste(img, (0, 0))
    transparent_to_show = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent_to_show.paste(img_to_show, (0, 0))
    if left_upper is True:
        transparent_to_show.paste(watermark_to_show, (0, 0), mask=watermark_to_show)
        transparent.paste(watermark, (0, 0), mask=watermark)
    elif left_bottom is True:
        transparent_to_show.paste(watermark_to_show, (0, 310), mask=watermark_to_show)
        transparent.paste(watermark, (0, b_height-50*img_size_scale), mask=watermark)
    elif right_bottom is True:
        transparent_to_show.paste(watermark_to_show, (430, 310), mask=watermark_to_show)
        transparent.paste(watermark, (b_width-50*img_size_scale, b_height-50*img_size_scale), mask=watermark)
    elif right_upper is True:
        transparent_to_show.paste(watermark_to_show, (430, 0), mask=watermark_to_show)
        transparent.paste(watermark, (b_width-50*img_size_scale, 0), mask=watermark)
    else:
        print_error(1)
        return None
    img_b = ImageTk.PhotoImage(transparent_to_show)
    panel = Label(image=img_b)
    panel.img = img_b
    panel.place(x=300, y=200)
    img_watermark_save = True


def save_img():
    global transparent, text_watermark_save, img_watermark_save, img
    if img_watermark_save is True:
        filename_save = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
        if filename_save == "":
            return None
        transparent = transparent.convert("RGB")
        transparent.save(filename_save)
    elif text_watermark_save is True:
        filename_save = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")
        if filename_save == "":
            return None
        img_to_save = img.convert("RGB")
        img_to_save.save(filename_save)


def openfilename():
    filename = filedialog.askopenfilename(title='"pen')
    return filename


def reset():
    global panel
    setup()
    panel.img = None


def left_bottom():
    global left_bottom, left_upper, right_bottom, right_upper
    left_bottom = True
    left_upper = False
    right_upper = False
    right_bottom = False


def left_upper():
    global left_bottom, left_upper, right_bottom, right_upper
    left_upper = True
    left_bottom = False
    right_upper = False
    right_bottom = False


def right_bottom():
    global left_bottom, left_upper, right_bottom, right_upper
    right_bottom = True
    left_upper = False
    left_bottom = False
    right_upper = False


def right_upper():
    global left_bottom, left_upper, right_bottom, right_upper
    right_upper = True
    right_bottom = False
    left_upper = False
    left_bottom = False


def retrieve_input():
    input_value = textBox.get("1.0", "end-1c")
    return input_value


def print_error(error_id):
    if error_id == 1:
        label = Label(root, text="Set where to place img watermark", font=("arial.ttf", 10), fg="red")
        label.place(x=450, y=60)
    if error_id == 2:
        label = Label(root, text="Set where to place text watermark", font=("arial.ttf", 10), fg="red")
        label.place(x=450, y=60)
    if error_id == 3:
        label = Label(root, text="Load your image", font=("arial.ttf", 10), fg="red")
        label.place(x=495, y=60)


root = Tk()
root.title("Watermarking app")
root.geometry("1100x800")

button1 = Button(root, bg="green", fg="white", width=15, text="Load image", command=open_img)
button1.place(x=10, y=20)
button2 = Button(root, bg="green", fg="white", width=15, text="Add text watermark", command=add_text_watermark)
button2.place(x=960, y=20)
button3 = Button(root, bg="green", fg="white", width=15, text="Save image", command=save_img)
button3.place(x=495, y=20)
button4 = Button(root, bg="green", fg="white", width=15, text="Add img watermark", command=add_img_watermark)
button4.place(x=960, y=60)

buttonCommit = Button(root, bg="green", fg="white", width=11, text="Commit",
                      command=retrieve_input)
buttonCommit.place(x=860, y=20)
textBox = Text(root, height=1, width=10)
textBox.pack()
textBox.place(x=760, y=20)

button_left_bottom = Button(root, bg="green", fg="white", width=15, text="Left Bottom", command=left_bottom)
button_left_bottom.place(x=960, y=100)
button_left_upper = Button(root, bg="green", fg="white", width=15, text="Left Upper", command=left_upper)
button_left_upper.place(x=960, y=140)
button_right_bottom = Button(root, bg="green", fg="white", width=15, text="Right Bottom", command=right_bottom)
button_right_bottom.place(x=960, y=180)
button_right_upper = Button(root, bg="green", fg="white", width=15, text="Right Upper", command=right_upper)
button_right_upper.place(x=960, y=220)
reset_button = Button(root, bg="green", fg="white", width=15, text="Reset", command=reset)
reset_button.place(x=960, y=260)
exit_button = Button(root, bg="green", fg="white", width=15, text="Close app", command=root.destroy)
exit_button.place(x=960, y=300)

measure = Label(root, font=("arial.ttf", int(0.75 * FONT_SIZE)), text="")
measure.place(x=1200, y=300)
label_scaled = Label(root, font=("arial.ttf", int(0.75 * FONT_SIZE)), text="")
label_scaled.place(x=1500, y=300)


root.mainloop()