from tkinter import *
from PIL import ImageTk, Image, ImageDraw, ImageFont
from tkinter import filedialog

SIZE = 500, 300
BACKGROUND_COLOR = "#94b5c0"
FONT = ("Arial", 10, "bold")
window = Tk()
window.title("Watermark App")
window.geometry("650x600")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
show_img, img, copy_img, clear = [], [], [], []
file_type = ""
# Allow Window to be resizable
# window.resizable(width=True, height=True)


def open_img():
    global show_img, img, copy_img, file_type
    # Select the Imagename  from a folder
    x = filedialog.askopenfilename(title='Open image')
    file_type = x.split(".")[1]
    # opens the image
    img = Image.open(x)
    copy_img = img.copy()
    # resize the image, thumbnail function returns none
    copy_img.thumbnail(SIZE, resample=3, reducing_gap=2.0)
    # PhotoImage class is used to add image to widgets, icons etc
    show_img = ImageTk.PhotoImage(copy_img)
    canvas.itemconfig(canvas_img, image=show_img)


def add_watermark():
    global img, copy_img, clear
    # Take a fresh copy of the original each time before you write on it
    clear = img.copy()
    # print(clear.size[0])
    a = ImageDraw.Draw(clear)
    w_text = txt_entry.get("1.0", END)
    txt_font = ImageFont.truetype("arial.ttf", int(round(clear.size[1]*0.04, 0)))
    print(txt_font.getsize(w_text))
    print(txt_font.font.getsize(w_text))
    img_x, img_y = clear.size[0]*0.95, clear.size[1]*0.95
    a.multiline_text((img_x, img_y), w_text, font=txt_font, fill='white', anchor='rs')
    # clear.show()
    #show text on canvas, need to work on the position. How to make sure that the text position on the canvas is
    # same as on the original image
    canvas_x, canvas_y = 250+copy_img.size[0]/2*0.9, 150+copy_img.size[1]/2
    canvas_font_size =int(round(copy_img.size[1]*0.04, 0))
    update_canvas_txt(canvas_x, canvas_y, w_text, canvas_font_size)


def save_watermark():
    global file_type, clear
    file = filedialog.asksaveasfilename(defaultextension=f".{file_type}", title="Select file", filetypes=(
        ('JPEG', ('*.jpg', '*.jpeg', '*.jpe')), ('PNG', '*.png'), ('BMP', ('*.bmp', '*.jdib')), ('GIF', '*.gif')))
    # <_io.TextIOWrapper name='C:/Users/echo/PycharmProjects/day 84 watermark/img/4.png' mode='w' encoding='cp1252'>
    if file is None:  # asksaveasfile return `None` if dialog closed with "cancel".
        return
    clear.save(file)


def update_canvas_txt(x, y, text, size):
    global canvas_text
    canvas.delete(canvas_text)
    canvas_text = canvas.create_text(x, y, text=text, font=("arial.ttf", size), fill='white', anchor="se")


# Create a button and place it into the window using grid layout
btn_open = Button(text='Open image', fg="#350b40", command=open_img, font=FONT, width=14, height=2)
btn_open.grid(row=0, column=0, padx=10, pady=10)

btn_save = Button(text='Save image', fg="#350b40", font=FONT, width=14, height=2, command=save_watermark)
btn_save.grid(row=1, column=0, padx=10, pady=10)


canvas = Canvas(width=500, height=300, bg=BACKGROUND_COLOR, highlightthickness=0)
img_1 = PhotoImage(file="./img/canvas.png")
canvas_img = canvas.create_image(250, 150, image=img_1)
# create blank text on canvas
canvas_text = canvas.create_text(250, 150, text="", font=("arial.ttf", 10), fill='white')
canvas.grid(column=0, row=3, columnspan=3, padx=20, pady=20)


txt_entry = Text(width=20, height=10, font=FONT)
# add placeholder to the text box
txt_entry.insert(END, 'Add text')
txt_entry.grid(row=0, column=1, columnspan=2, rowspan=3)

save_txt = Button(text="Save watermark", font=FONT, width=14, height=2, fg="#350b40", command=add_watermark)
save_txt.grid(column=0, row=2,  padx=10, pady=10)


window.mainloop()