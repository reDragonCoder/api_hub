# ------------ LIBRARIES ------------
# Libraries for sending HTTP requests
import requests
from urllib.request import urlopen
from requests.exceptions import HTTPError
# Library for handling image data
from PIL import Image, ImageTk
# Library for creating a GUI interface
import tkinter as tk
import tkinter.messagebox as msgbox
# Library for using X API
import tweepy
import webbrowser
# -----------------------------------

# ---------- API ENDPOINTS ----------
nasa_url = "https://api.nasa.gov/planetary/apod"
pokemon_url = "https://pokeapi.co/api/v2"
chuckN_url = "https://api.chucknorris.io/jokes/random"
# -----------------------------------

# ------------- API KEYS ------------
nasa_key = "RjeNVFxhx2TnbLN8OZcqdQ17LBMqRxGtSyacFM4s"
consumerX_key='JHnRw8Auqu4SNUsIQ1EpzshR6'
consumerX_secret='kmYE6ZgPBikmMZtaBzsNsF83Xqk4TFHHAvvEh0fwRy8zkrmQ5t'
bearerX_token='AAAAAAAAAAAAAAAAAAAAAEoTzgEAAAAAbhrYoe0TlP1GFC0dsBP1KThJvoc%3DyAanX3UCYEpIQyTrKzLpFZDdbgxikC7YEc18uKvg0bkkTuQpTs' 
accessX_token='1893874559163527168-sajhzV0mFSkaZQWOC8MxI9Lh33wx8F'
accessX_token_secret='nqdLvVaTUBLLzGVkbQwmAoK5MA2xM1YBfAmiry6KdYjyY'
# -----------------------------------

# ---------- GUI FUNCTIONS ----------
def center_window(win, width, height):
    win.geometry(f"{width}x{height}")
    win.update_idletasks()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

def show_frame(frame):
    reset_fields1()
    reset_fields2()
    reset_fields3()
    reset_fields4()
    # Hide all frames before showing the current one
    frame0.pack_forget()
    frame1.pack_forget()
    frame2.pack_forget()
    frame3.pack_forget()
    frame4.pack_forget()

    # Show the selected frame
    frame.pack(expand=True, fill="both")

# -----------------------------------

# ---- APIs FUNCTIONS & Classes -----
# NASA API
def get_astronomyPic(date):
    url = f"{nasa_url}?api_key={nasa_key}&date={date}"

    # GET (request data from the server)
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an exception for HTTP errors
    except requests.exceptions.HTTPError as errh:
        msgbox.showerror("Error", f"HTTP Error: {errh}")
        return None
    except requests.exceptions.RequestException as e:
        msgbox.showerror("Error", "Error")
        return None
    
    if response.status_code == 200:
        # response.json() retrieves the data as a dictionary
        astronomyPic_data = response.json()
        return astronomyPic_data
    else:
        msgbox.showerror("Error", f"Failed to retrieve data: {response.status_code}")
        return None

def show_astronomyPic_data():
    yyyy = entryYear.get()
    mm = entryMonth.get()
    dd = entryDay.get()

    # Validate year, month, and day input
    try:
        date = f"{int(yyyy)}-{int(mm)}-{int(dd)}"
    except ValueError:
        msgbox.showerror("Error", "Invalid date input")
        return

    astronomyPic_info = get_astronomyPic(date)

    if astronomyPic_info:
        # Display pic info
        title1_label.config(text=f"Title: {astronomyPic_info['title'].capitalize()}")
        date_label.config(text=f"Date: {astronomyPic_info['date']}")

        explanation_textbox.config(state=tk.NORMAL)
        explanation_textbox.delete(1.0, tk.END)
        explanation_textbox.insert(tk.END, f"{astronomyPic_info['explanation']}")
        explanation_textbox.config(state=tk.DISABLED)

        # Display image/picture
        url_image = astronomyPic_info['url']
        if url_image and url_image.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                image = Image.open(urlopen(url_image))
                new_size = (300, 300)
                image = image.resize(new_size)  # Resize to fit the window
                photo = ImageTk.PhotoImage(image)
                image1_label.config(image=photo)
                image1_label.image = photo  # Keeping reference to avoid garbage collection
            except Exception as e:
                msgbox.showerror("Error", "Error loading picture")
                image1_label.image = None
        else:
            msgbox.showerror("Error", "Image URL is invalid")
            image1_label.image = None
    else:
        msgbox.showerror("Error", "Error retrieving data")
        title1_label.config(text="")
        date_label.config(text="")
        explanation_textbox.delete(1.0, tk.END)
        image1_label.config(image='')  # Reset image to None
        image1_label.image = None

def reset_fields1():
    entryYear.delete(0, tk.END)
    entryMonth.delete(0, tk.END)
    entryDay.delete(0, tk.END)
    title1_label.config(text="")
    date_label.config(text="")
    explanation_textbox.config(state="normal")
    explanation_textbox.delete("1.0", tk.END)
    explanation_textbox.config(state="disabled")
    image1_label.config(image='')  # Resets the image to none
    image1_label.image = None

# Pokemon API
def get_pokemon_info(name):
    url = f"{pokemon_url}/pokemon/{name}"

    # GET (request data from the server)
    response = requests.get(url)
    
    if response.status_code == 200:
        # response.json() retrieves all pokemon info as a dictionary
        pokemon_data = response.json()
        return pokemon_data
    else:
        msgbox.showerror("Error", f"Failed to retrieve data")    
        return None  

def show_pokemon_info():
    name = entry2.get().lower()
    pokemon_info = get_pokemon_info(name)

    if pokemon_info:
        # Update window title
        root.title(f"{pokemon_info['name'].capitalize()} Info")

        # Display Pokemon info
        name_label2.config(text=f"Name: {pokemon_info['name'].capitalize()}")
        id_label2.config(text=f"ID: {pokemon_info['id']}") 
        height_label2.config(text=f"Height: {pokemon_info['height']} decimetres") 
        weight_label2.config(text=f"Weight: {pokemon_info['weight']} hectograms") 

        # Display Pokemon image
        url_image = pokemon_info['sprites']['other']['official-artwork']['front_default']
        if url_image:
            try:
                image = Image.open(urlopen(url_image))
                new_size = (200, 200)
                image = image.resize(new_size)
                photo = ImageTk.PhotoImage(image)
                image_label2.config(image=photo)
                image_label2.image = photo  # Keeping reference to avoid garbage collection
            except Exception as e:
                msgbox.showerror("Error", f"Error loading image: {e}")
                image_label2.config(text="Error loading image")
                image_label2.image = None
        else:
            msgbox.showerror("Error", "No image available for this Pokemon")
            image_label2.config(text="No image available")
            image_label2.image = None
    else:
        msgbox.showerror("Error", "Pokemon not found")
        name_label2.config(text="")
        id_label2.config(text="")
        height_label2.config(text="")
        weight_label2.config(text="")
        types_label2.config(text="")
        image_label2.config(image='')
        image_label2.image = None

def reset_fields2():
    entry2.delete(0, tk.END)
    name_label2.config(text="")
    id_label2.config(text="")
    height_label2.config(text="")
    weight_label2.config(text="")
    types_label2.config(text="")
    image_label2.config(image='')
    image_label2.image = None

# X API
client=tweepy.Client(
    bearer_token=bearerX_token,
    consumer_key=consumerX_key,
    consumer_secret=consumerX_secret,
    access_token=accessX_token,
    access_token_secret=accessX_token_secret
)

auth=tweepy.OAuth1UserHandler(consumerX_key, consumerX_secret, accessX_token, accessX_token_secret)
api=tweepy.API(auth)

def post_tweet(text):
    max_chars = 279
    current_text = textbox_Tweet.get("1.0", tk.END)
    if len(current_text) > max_chars:
        textbox_Tweet.delete("1.0", tk.END)
        textbox_Tweet.insert("1.0", current_text[:max_chars])
        msgbox.showerror("Error", "Max. character limit exceeded")
        return "break"
    
    try:
        client.create_tweet(text=text)
        msgbox.showinfo("Success", "Tweet uploaded successfully....")
    except tweepy.TweepyException as e:
        msgbox.showerror("Error", f"Error uploading tweet: {e}")

def open_profile():
    webbrowser.open("https://nitter.net/smartfoxbot")

def reset_fields3():
    textbox_Tweet.delete("1.0", tk.END)

# Chuck Norris API
def get_ChuckNJoke():
    url = chuckN_url

    try:
        response = requests.get(url)
        response.raise_for_status() 
    except requests.exceptions.HTTPError as errh:
        msgbox.showerror("Error", f"HTTP Error: {errh}")
        return None
    except requests.exceptions.RequestException as e:
        msgbox.showerror("Error", "Error")
        return None
    
    if response.status_code == 200:
        # response.json() retrieves the data as a dictionary
        cnJoke = response.json()
        return cnJoke
    else:
        msgbox.showerror("Error", f"Failed to retrieve data: {response.status_code}")
        return None

def show_ChuckNJoke():
    joke = get_ChuckNJoke()

    if joke:
        textbox_Joke4.config(state=tk.NORMAL)
        textbox_Joke4.delete(1.0, tk.END)
        textbox_Joke4.insert(tk.END, f"{joke['value']}")
        textbox_Joke4.config(state=tk.DISABLED)

    else:
        msgbox.showerror("Error", "Error retrieving data")
        textbox_Joke4.delete(1.0, tk.END)

def reset_fields4():
    textbox_Joke4.config(state="normal")
    textbox_Joke4.delete("1.0", tk.END)
    textbox_Joke4.config(state="disabled")


# -----------------------------------

# ----------- GUI CONFIG ------------
root = tk.Tk()
root.title("API Hub")

center_window(root, 900, 700)

container = tk.Frame(root)
container.pack(fill="both", expand=True)

# Menu frame
frame0 = tk.Frame(container)
frame0.pack(expand=True, fill="both")
# NASA Astronomy Pic frame
frame1 = tk.Frame(container)
frame1.pack(expand=True, fill="both")
# Pokedex frame 
frame2 = tk.Frame(container)
frame2.pack(expand=True, fill="both")
# Twitter Bot frame 
frame3 = tk.Frame(container)
frame3.pack(expand=True, fill="both")
# Chuck Norris frame
frame4 = tk.Frame(container)
frame4.pack(expand=True, fill="both")

# Menu Content
title0_label = tk.Label(frame0, text="APIs Hub", font=("Courier", 40))
title0_label.pack(pady=40)

labelEndpoint1 = tk.Label(frame0, text="EndPoint 1 - GET", font=("Courier", 20))
labelEndpoint1.pack(pady=20)

button_changeFrame1 = tk.Button(frame0, text="  Astronomy Picture Of The Day  ", command=lambda: show_frame(frame1), font=("Courier", 12)) 
button_changeFrame1.pack(padx=10)

labelEndpoint2 = tk.Label(frame0, text="EndPoint 2 - GET", font=("Courier", 20))
labelEndpoint2.pack(pady=20)

button_changeFrame2 = tk.Button(frame0, text="             Pokedex            ", command=lambda: show_frame(frame2), font=("Courier", 12)) 
button_changeFrame2.pack(padx=20)

labelEndpoint3 = tk.Label(frame0, text="EndPoint 3 - POST", font=("Courier", 20))
labelEndpoint3.pack(pady=20)

button_changeFrame3 = tk.Button(frame0, text="          Twitter Bot           ", command=lambda: show_frame(frame3), font=("Courier", 12)) 
button_changeFrame3.pack(padx=20)

labelEndpoint4 = tk.Label(frame0, text="EndPoint 4 - GET (extra)", font=("Courier", 20))
labelEndpoint4.pack(pady=20)

button_changeFrame3 = tk.Button(frame0, text="      Chuck Norris Jokes         ", command=lambda: show_frame(frame4), font=("Courier", 12)) 
button_changeFrame3.pack(padx=20)

# NASA Content
labelEntries_frame1 = tk.Frame(frame1)
labelEntries_frame1.pack(pady=5)

labelYear = tk.Label(labelEntries_frame1, text="Year (YYYY format)", font=("Courier", 12))
labelYear.pack(side=tk.LEFT, padx=10)

labelMonth = tk.Label(labelEntries_frame1, text="Month (MM format)", font=("Courier", 12))
labelMonth.pack(side=tk.LEFT, padx=30)

labelDay = tk.Label(labelEntries_frame1, text="Day (DD format)", font=("Courier", 12))
labelDay.pack(side=tk.LEFT, padx=10)

entry_frame1 = tk.Frame(frame1)
entry_frame1.pack(pady=5)

entryYear = tk.Entry(entry_frame1, font=("Courier", 12))
entryYear.pack(side=tk.LEFT, padx=5)

entryMonth = tk.Entry(entry_frame1, font=("Courier", 12))
entryMonth.pack(side=tk.LEFT, padx=5)

entryDay = tk.Entry(entry_frame1, font=("Courier", 12))
entryDay.pack(side=tk.LEFT, padx=5)

button_frame21 = tk.Frame(frame1)
button_frame21.pack(pady=5)

button_search21 = tk.Button(button_frame21, text="Search", command=show_astronomyPic_data, font=("Courier", 12))
button_search21.pack(side=tk.LEFT, padx=5)

button_reset2 = tk.Button(button_frame21, text="Reset", command=reset_fields1, font=("Courier", 12))
button_reset2.pack(side=tk.LEFT, padx=5)

button_back1 = tk.Button(frame1, text="Back", command=lambda: show_frame(frame0), font=("Courier", 12))
button_back1.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

title1_label = tk.Label(frame1, text="", font=("Courier", 12))
title1_label.pack(pady=5)

date_label = tk.Label(frame1, text="", font=("Courier", 12))
date_label.pack(pady=5)

explanation_textbox = tk.Text(frame1, wrap=tk.WORD, font=("Courier", 12), height=10, width=70)
explanation_textbox.pack(pady=5)
explanation_textbox.config(state=tk.DISABLED)

image1_label = tk.Label(frame1)
image1_label.pack(pady=5)

# Pokedex Content 
entry2 = tk.Entry(frame2, font=("Courier", 16))
entry2.pack(pady=40)

button_frame2 = tk.Frame(frame2)
button_frame2.pack(pady=5)

button_search2 = tk.Button(button_frame2, text="Search", command=show_pokemon_info, font=("Courier", 16))
button_search2.pack(side=tk.LEFT, padx=5)

button_reset2 = tk.Button(button_frame2, text="Reset", command=reset_fields2, font=("Courier", 16))
button_reset2.pack(side=tk.LEFT, padx=5)

name_label2 = tk.Label(frame2, text="", font=("Courier", 16))
name_label2.pack(pady=15)

id_label2 = tk.Label(frame2, text="", font=("Courier", 16))
id_label2.pack(pady=5)

height_label2 = tk.Label(frame2, text="", font=("Courier", 16))
height_label2.pack(pady=5)

weight_label2 = tk.Label(frame2, text="", font=("Courier", 16))
weight_label2.pack(pady=5)

types_label2 = tk.Label(frame2, text="", font=("Courier", 16))
types_label2.pack(pady=5)

image_label2 = tk.Label(frame2)
image_label2.pack(pady=15)

button_back2 = tk.Button(frame2, text="Back", command=lambda: show_frame(frame0), font=("Courier", 16))
button_back2.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

# Twitter Bot Content 
label_profileInfo3 = tk.Label(frame3, text="Post a tweet", font=("Courier", 16))
label_profileInfo3.pack(pady=20)

textbox_Tweet = tk.Text(frame3, wrap=tk.WORD, font=("Courier", 12), height=10, width=70, state="normal")
textbox_Tweet.pack(pady=10)

button_reset3 = tk.Button(frame3, text="Reset", command=lambda: reset_fields3(), font=("Courier", 16))
button_reset3.pack(pady=10)

button_submitInfo3 = tk.Button(frame3, text="Submit", command=lambda: post_tweet(textbox_Tweet.get("1.0", tk.END)), font=("Courier", 16))
button_submitInfo3.pack(pady=10)

button_goToProfile3 = tk.Button(frame3, text="Go to profile", command=lambda: open_profile(), font=("Courier", 16))
button_goToProfile3.pack(pady=10)

button_back3 = tk.Button(frame3, text="Back", command=lambda: show_frame(frame0), font=("Courier", 16))
button_back3.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

# Chuck Norris Content
label_Title4 = tk.Label(frame4, text="Chuck Norris Jokes", font=("Courier", 40))
label_Title4.pack(pady=50)

textbox_Joke4 = tk.Text(frame4, wrap=tk.WORD, font=("Courier", 12), height=10, width=70, state="disabled")
textbox_Joke4.pack(pady=20)

button_generate4 = tk.Button(frame4, text="Generate", command=lambda: show_ChuckNJoke(), font=("Courier", 16))
button_generate4.pack(pady=20)

button_reset4 = tk.Button(frame4, text="Reset", command=lambda: reset_fields4(), font=("Courier", 16))
button_reset4.pack(pady=10)

button_back4 = tk.Button(frame4, text="Back", command=lambda: show_frame(frame0), font=("Courier", 16))
button_back4.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)


# Show the menu frame initially
show_frame(frame0)

root.mainloop()
