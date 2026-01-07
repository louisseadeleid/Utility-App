
from tkinter import * # Tkinter library import to create the windows
import requests # For making HTTP requests to APIs
from PIL import Image, ImageTk# Pillow library so i can import images from the api
from io import BytesIO # To convert image data from URL so it can translate to laptop
root = Tk() # Create the main Tkinter window object
root.geometry("600x1000") # Set window size
root.config(bg="#FFE6EE")  # Set background color to a light pink 
api = "8dcfefcd3584cd8eb2b7527c86bcf038"  # this is used as my personal api key used for the weather apo

def search(): 
    """this searches the recipes and this is connected to the search button 
    so when it runs this is called"""
    mealname = entry.get() # Get text input
    if mealname == "": # Validate input so if user failed to search the name, it will print or configure the text
        resultl.config(text="Please enter a meal name")
        return 

    # this requests the meals data from the mealdb api
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={mealname}"
    response = requests.get(url)  # Send GET request to the API
    if response.status_code == 200:  # If the request was successful
        global mealsinfo  #  global variable to store meals so that this variable can be used everywhere in the code
        data = response.json() # Convert JSON response to Python 
        mealsinfo = data["meals"]# Extract the 'meals' list form the db

        if mealsinfo is None:  # If no meal is found the following will be done so it wont error
            resultl.config(text="No recipe found")
            imagecont.config(image="")   # Clear the image label
            instructions.delete("1.0", END)  # Clear instructions Text widget
            ingredientslist.delete("1.0", END)  # Clear ingredients Text widget
            listbox.delete(0, END)# Clear Listbox
            return
        # Fill Listbox with meal names if multiple meals are returned
        listbox.delete(0, END)  # Clear existing texts in the listbox
        for meal in mealsinfo:
            listbox.insert(END, meal["strMeal"])
        showmeal(0) # Display the first meal by default

    else:   # If API request failed it will configure saying that its an error
        resultl.config(text="Error getting recipe")


def showmeal(index):
    """Display meal details (name, instructions, ingredients, image) at the given index."""
    meal = mealsinfo[index]  # Get meal from the global list by index
    resultl.config(text=meal["strMeal"])  # Update meal name label

    # Display cooking instructions
    instructions.delete("1.0", END)   # Clear previous instructions so that nothing iwll overlap
    instructions.insert(END, meal["strInstructions"])  # Insert new instructions

    # Display ingredients
    ingredientslist.delete("1.0", END)  # Clear previous ingredients so no overlapping
    ingredients = [] # this creates a list that ensures that there is nothing inside
    for i in range(1, 21):  # Meals can have up to 20 ingredients
        ing = meal.get(f"strIngredient{i}")   # Get ingredient
        meas = meal.get(f"strMeasure{i}") # Get measurement from the database
        if ing and ing.strip() != "":  # Check ingredient is not empty
            ingredients.append(f"{ing} - {meas}")  # Combine ingredient & measure
    ingredientslist.insert(END, "\n".join(ingredients))  # Display in Text widget

    # Display meal image
    image = meal["strMealThumb"] # Get URL of meal thumbnail and this is from the database
    img_data = requests.get(image).content # Download image data
    img = Image.open(BytesIO(img_data))# Convert image data to PIL Image
    img = img.resize((150, 150)) # Resize image to fit GUI
    photo = ImageTk.PhotoImage(img)# Convert PIL image to Tkinter-compatible image
    imagecont.config(image=photo) # Set image label to the new photo
    imagecont.image = photo  # Keep reference to avoid garbage collection


def select(event):
    """Trigger when user selects a meal from the Listbox and then show the meal details if it does 
    exist"""
    if listbox.curselection():   # Check if a selection exists
        index = listbox.curselection()[0]  # Get the index of the selected meal
        showmeal(index)  

def randomrecipe():
    """Gets a random meal from TheMealDB APi and displays its details"""
    url = "https://www.themealdb.com/api/json/v1/1/random.php"
    response = requests.get(url).json() # Send GET request and convert JSON
    global mealsinfo # ensures that this variable can be used all throughout the code
    mealsinfo = response["meals"] # Store random meal in global variable
    # Update Listbox with the random meal
    listbox.delete(0, END)
    for meal in mealsinfo:
        listbox.insert(END, meal["strMeal"])
    showmeal(0) # Show the random meal automatically
def recweather():
    """Suggest a recipe based on the current temperature of the entered city. So the recipes given 
    would be solely based on the temparature given with the conditions i set"""
    city = citye.get() # Get city name from Entry widget
    if city == "": # ensures that the user will place a valid city
        resultl.config(text="enter a valid city!!!")
        return
    # Request current weather from the weather API, make sure that your api key in the end so you can access the weather
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api}"
    response = requests.get(weather_url) 
    if response.status_code != 200:
        resultl.config(text="Error to get weather")
        return

    weatherdata = response.json() # Convert JSON response to Python dict
    temp = weatherdata["main"]["temp"]  # Extract current temperature
    # Suggest recipe category based on temperature
    if temp < 18:
        suggested = "Soup"
    elif temp > 28:
        suggested = "Salad"
    else:
        suggested = "Chicken"  # Default moderate meal

    # Update meal entry with suggestion and automatically search for recipe
    resultl.config(text=f"Current Temp: {temp}°C and my suggestion: {suggested}")
    entry.delete(0, END)   # Clear meal Entry box
    entry.insert(0, suggested) # Insert suggested recipe
    search()  # Automatically fetch suggested recipe

# Label for searching the meal and asking whats the name
Label(root, text="Meal name?", font=("Helvetica", 20, "bold"), fg="#BA507C", bg="#FFE6EE").pack(pady=5)
# Entry widget for user to type meal name
entry = Entry(root, width=30, font=("Helvetica", 16))
entry.pack(pady=5)
# Search recipe button 
searchb = Button(root, text="Search Recipe", font=("Helvetica", 16, "bold"),  fg="#BA507C", bg="#FFE6EE", command=search)
searchb.pack(pady=5)
# Random recipe button
randombutton = Button(root, text="Random Recipe", font=("Helvetica", 16, "bold"),  fg="#BA507C", bg="#FFE6EE", command=randomrecipe)
randombutton.pack(pady=5)
# Weather suggestion label
Label(root, text="Enter City for Recipe based on your temperature", font=("Helvetica", 16, "bold"), fg="#BA507C", bg="#FFE6EE").pack(pady=5)
# Entry widget for city name
citye = Entry(root, width=30, font=("Helvetica", 16))
citye.pack(pady=5)
# Weather suggestion button
weatherb = Button(root, text="Suggest Recipe by Weather", font=("Helvetica", 16, "bold"), fg="#BA507C", bg="#FFE6EE", command=recweather)
weatherb.pack(pady=5)
# Listbox to display multiple meals returned by search
listbox = Listbox(root, width=50, height=3)
listbox.pack(pady=10)
listbox.bind("<<ListboxSelect>>", select)  # Bind selection event to select() function
# Label to display meal image
imagecont = Label(root)
imagecont.pack(pady=10)
# Label to display meal name
resultl = Label(root, text="", font=("Helvetica", 20, "bold"), fg="#BA507C", bg="#FFE6EE")
resultl.pack(pady=5)
# Ingredients label
Label(root, text="Ingredients:", font=("Helvetica", 16, "bold"), fg="#BA507C", bg="#FFE6EE").pack()
# Text widget to display ingredients
ingredientslist = Text(root, wrap=WORD, width=55, height=5)
ingredientslist.pack(pady=5)
# Instructions label
Label(root, text="Instructions:", font=("Helvetica", 16, "bold"), fg="#BA507C", bg="#FFE6EE").pack()
# Text widget to display cooking instructions
instructions = Text(root, wrap=WORD, width=55, height=10)
instructions.pack(pady=10)

root.mainloop()  # Place this to keep the GUI running and loop it
