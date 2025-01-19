from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
import win32clipboard
import sys
import emoji

###print(tk.TkVersion)

# Store the image references globally
image_refs = {}

emoji_size = 100


# Get arguments from the command line

item1_num = 3
if (len(sys.argv) > 1):
    item1_num = int(sys.argv[1])
 
item2_num = 4 
if (len(sys.argv) > 2):
    item2_num = int(sys.argv[2])

switch = False
if (len(sys.argv) > 3):
    switch = sys.argv[3].lower() in ('switch')  # Convert string to boolean

emoji_1 = '🍎'    
if (len(sys.argv) > 4):
    emoji_1 = sys.argv[4]
    print(f"emoji_1={emoji.demojize(emoji_1)}")
    
emoji_2 = '🍐'    
if (len(sys.argv) > 5):
    emoji_2 = sys.argv[5]
    print(f"emoji_2={emoji.demojize(emoji_2)}")




def emoji_img(size, emoji_text, count_text='1'):
    font_emoji = ImageFont.truetype("seguiemj.ttf", size=int(round(size*36/96, 0))) 
    font_count = ImageFont.truetype("seguiemj.ttf", size=int(round(size*36/96, 0))) 
    
    # Calculate the width and height for both parts of the text
    im = Image.new("RGBA", (size*10, size*2), (255, 255, 255, 0))
    draw = ImageDraw.Draw(im)
    
    # Calculate the width and height for both parts of the text using textbbox (new method)
    emoji_bbox = draw.textbbox((0, 0), emoji_text, font=font_emoji)
    emoji_width = emoji_bbox[2] - emoji_bbox[0]
    emoji_height = emoji_bbox[3] - emoji_bbox[1]
    
    # Draw the emoji part (centered)
    draw.text(((im.width - emoji_width) / 2, (im.height - emoji_height) / 2), emoji_text, font=font_emoji, embedded_color=True)
    
    # Calculate the width and height for the count text
    count_bbox = draw.textbbox((0, 0), count_text, font=font_count)
    count_width = count_bbox[2] - count_bbox[0]
    count_height = count_bbox[3] - count_bbox[1]
    
    horizontal_offset = 20  
    vertical_offset = 20  
    
    # Draw the count part in black color below the emoji
    ##draw.text(((im.width - count_width) / 2 , (im.height - count_height) / 2 + emoji_height + ##vertical_offset), count_text, font=font_count, fill="black")
    
    draw.text(((im.width + emoji_width + count_width) / 2, (im.height - count_height) / 2 ), count_text, font=font_count, fill="black")
    
    
    # Keep the reference to the image object to prevent garbage collection
    img_tk = ImageTk.PhotoImage(im)
    image_refs[emoji_text] = img_tk  # Save reference for later use
    return img_tk

  
    
def copy():
    emoji_data = button['text']
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, emoji_data)
    win32clipboard.CloseClipboard()
    print("Copied!", emoji_data)

def calculate_fruits():
    # Combine all items into a single string
    total_items = emoji_text1 + emoji_text2
    if (switch == True):
        total_items = emoji_text2 + emoji_text1
    emoji3 = emoji_img(emoji_size, total_items, "(" + str(item2_num + item1_num) + ")")
    result_label.config(image=emoji3, text=total_items)
    
def createEmojisSet(emoj='', num=1):
    emojis = emoj * num
    return emojis
    
 

# Create main window
root = tk.Tk()
root.title("Item Counter")

# Set the initial window size based on the amount of content you expect
root.geometry("800x600")  # You can adjust this to fit your content better

# Create Canvas widget
##canvas = tk.Canvas(root, width=600, height=400, bg="white")
##canvas.pack()

# Display item1, plus sign, item2, and their counts

emoji_text1 = createEmojisSet(emoj=emoji_1, num=item1_num) 

emoji1 = emoji_img(emoji_size, emoji_text1, "(" + str(item1_num) + ")" )
emoji1_label = tk.Label(root, image=emoji1, text=emoji_text1 )


plus_label = tk.Label(root, text="+ (add)", font=("Arial", 24))

emoji_text2=createEmojisSet(emoj=emoji_2, num=item2_num)
emoji2 = emoji_img(emoji_size, emoji_text2, "(" + str(item2_num) + ")")
emoji2_label = tk.Label(root, image=emoji2, text=emoji_text2)

if (switch == True):
    emoji2_label.pack()
    plus_label.pack()
    emoji1_label.pack()
else:
    emoji1_label.pack()
    plus_label.pack()
    emoji2_label.pack()



# Add button to calculate total fruits
calculate_button = tk.Button(root, text="Show All Items", command=calculate_fruits, bg="black", fg="white", font=("Arial", 14))
calculate_button.pack(pady=10)

# Label to display result
result_label = tk.Label(root, text="", font=("Segoe UI Emoji", 24))
result_label.pack()


# Adjust window size after packing the content to ensure it fits
##root.update_idletasks()
##root.geometry(f"{root.winfo_width()}x{root.winfo_height()}")  # Adjust window size to content


# Run the Tkinter event loop
root.mainloop()