#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 20:50:13 2026

@author: winsicheng
"""

from tkinter import * # Tkinter library import to create the windows
import requests # For making HTTP requests to APIs
from PIL import Image, ImageTk# Pillow library so i can import images from the api
from io import BytesIO # To convert image data from URL so it can translate to laptop
root = Tk() # Create the main Tkinter window object
root.geometry("600x1000") # Set window size
root.config(bg="#FFE6EE")  # Set background color to a light pink 
api = "8dcfefcd3584cd8eb2b7527c86bcf038"  # this is used as my personal api key used for the weather apo


class MealApp:
    """This class handles all meal related functions including search, random meals,
    displaying ingredients, instructions, images, and weather based recipe suggestions."""
    
    def __init__(self):
        self.mealsinfo = []  # creats an empty list to store meal data from API

    def search(self):
        """Search meals using MealDB API based on user input in the entry box."""
        mealname = entry.get()  # Get text input from the entry widget
        if mealname == "":  # Check if user did not type anything
            resultl.config(text="Please enter a meal name")  # Display error message
            return  # Exit the function to prevent further processing

        # Construct the MealDB API URL using the meal name
        url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={mealname}"
        response = requests.get(url)  # gets the request to the API
        if response.status_code == 200:  # Check if request was successful )
            data = response.json()  # Convert JSON response to Python dictionary
            self.mealsinfo = data["meals"]  # Extract the list of meals from JSON

            if self.mealsinfo is None:  # If no meals are found
                resultl.config(text="No recipe found")  # Inform the user
                imagecont.config(image="")  # Clear the image label
                instructions.delete("1.0", END)  # Clear instructions text widget
                ingredientslist.delete("1.0", END)  # Clear ingredients text widget
                listbox.delete(0, END)  # Clear listbox of meal names
                return  # Exit function to avoid errors

            # Fill listbox with meal names when multiple meals are returned
            listbox.delete(0, END)  # Clear previous listbox entries
            for meal in self.mealsinfo:  # Iterate through meals
                listbox.insert(END, meal["strMeal"])  # Insert meal names into listbox
            self.showmeal(0)  # Automatically show the first meal in the list
        else:
            resultl.config(text="Error getting recipe")  # Display error if API request fails

    def showmeal(self, index):
        """Display the selected meal's details: name, ingredients, instructions, and image."""
        meal = self.mealsinfo[index]  # Get the meal dictionary at the given index
        resultl.config(text=meal["strMeal"])  # Update meal name label

        # Display instructions
        instructions.delete("1.0", END)  # Clear previous instructions
        instructions.insert(END, meal["strInstructions"])  # Insert new instructions

        # Display ingredients
        ingredientslist.delete("1.0", END)  # Clear previous ingredients
        ingredients = []  # Initialize empty list to store ingredient strings
        for i in range(1, 21):  # MealDB supports up to 20 ingredients per meal
            ing = meal.get(f"strIngredient{i}")  # Get ingredient name
            meas = meal.get(f"strMeasure{i}")  # Get measurement for the ingredient
            if ing and ing.strip() != "":  # Check if ingredient exists and is not empty
                ingredients.append(f"{ing} - {meas}")  # Combine ingredient and measurement
        ingredientslist.insert(END, "\n".join(ingredients))  # Display all ingredients in Text widget

        # Display meal image
        imageu = meal["strMealThumb"]  # Get the URL of the meal image
        imginfo = requests.get(imageu).content  # Download image as bytes
        img = Image.open(BytesIO(imginfo))  # Convert bytes into a PIL Image object
        img = img.resize((150, 150))  # Resize image to fit GUI nicely
        photo = ImageTk.PhotoImage(img)  # Convert PIL Image to Tkinter-compatible image
        imagecont.config(image=photo)  # Display image in label
        imagecont.image = photo  # Keep a reference to avoid garbage collection

    def select(self, food):
        """Handle event when user clicks/selects a meal from the listbox."""
        if listbox.curselection():  # Check if a selection exists
            index = listbox.curselection()[0]  # Get the index of selected meal
            self.showmeal(food)  # Show meal details

    def randomrecipe(self):
        """Get and display a random meal from MealDB API and shows its ingredients and instructions"""
        url = "https://www.themealdb.com/api/json/v1/1/random.php"  # API endpoint for random meal
        response = requests.get(url).json()  # Send the request to convert JSON
        self.mealsinfo = response["meals"]  # Store random meal in mealsinfo

        # Update Listbox with the random meal
        listbox.delete(0, END)  # Clear listbox
        for meal in self.mealsinfo:  # Iterate through meals (usually 1)
            listbox.insert(END, meal["strMeal"])  # Insert meal name
        self.showmeal(0)  # Automatically show the meal

    def recweather(self):
        """Suggest a recipe based on current city temperature using OpenWeatherMap API."""
        city = citye.get()  # Get city name from entry widget
        if city == "":  # Validate city input
            resultl.config(text="Enter a valid city!!!")
            return

        # Construct API URL for weather
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api}"
        response = requests.get(weather_url)  # Send get request
        if response.status_code != 200:  # Check if request was successful
            resultl.config(text="Error getting weather")
            return

        weatherdata = response.json()  # Convert JSON to Python
        temp = weatherdata["main"]["temp"]  # Extract current temperature

        # Suggest recipe based on temperature
        if temp < 18:
            suggested = "Soup"  # Cold weather for hot meal
        elif temp > 28:
            suggested = "Salad"  # Hot weather for light meal
        else:
            suggested = "Chicken"  # Moderate temperature for default meal

        # Update entry with suggested meal and search it
        resultl.config(text=f"Current Temp: {temp}°C → Suggestion: {suggested}")
        entry.delete(0, END)  # Clear previous meal name
        entry.insert(0, suggested)  # Insert suggested meal
        self.search()  # Automatically search and display meal details

app = MealApp()  # calls the object class to run the app


""" The following would be the GUI design which follows the syntax. Root is the variable 
for the object and fg means the color for the text and bg would be the background color of the text
.pack is used to format the label, buttons, etc."""

# Meal search label
Label(root, text="Meal name?", font=("Helvetica", 20, "bold"),
      fg="#BA507C", bg="#FFE6EE").pack(pady=5)
entry = Entry(root, width=30, font=("Helvetica", 16))  # Entry widget for meal name
entry.pack(pady=5)

# Search button
searchb = Button(root, text="Search Recipe", font=("Helvetica", 16, "bold"),
                 fg="#BA507C", bg="#FFE6EE", command=app.search)
searchb.pack(pady=5)

# Random meal button
randombutton = Button(root, text="Random Recipe", font=("Helvetica", 16, "bold"),
                      fg="#BA507C", bg="#FFE6EE", command=app.randomrecipe)
randombutton.pack(pady=5)

# Weather suggestion label
Label(root, text="Enter City for Recipe based on your temperature",
      font=("Helvetica", 16, "bold"), fg="#BA507C", bg="#FFE6EE").pack(pady=5)
citye = Entry(root, width=30, font=("Helvetica", 16))  # Entry widget for city name
citye.pack(pady=5)

# Weather button
weatherb = Button(root, text="Suggest Recipe by Weather", font=("Helvetica", 16, "bold"), fg="#BA507C", bg="#FFE6EE", command=app.recweather) 
# command is used to run the recweather function

weatherb.pack(pady=5)
# Listbox for multiple meal results
listbox = Listbox(root, width=50, height=3)
listbox.pack(pady=10)
listbox.bind("<<ListboxSelect>>", app.select)  # Bind selection  to select() method

# Label to display meal image
imagecont = Label(root)
imagecont.pack(pady=10)
# Label to display meal name
resultl = Label(root, text="", font=("Helvetica", 20, "bold"),
                fg="#BA507C", bg="#FFE6EE")
resultl.pack(pady=5)

# Ingredients label and Text widget
Label(root, text="Ingredients:", font=("Helvetica", 16, "bold"),
      fg="#BA507C", bg="#FFE6EE").pack()
ingredientslist = Text(root, wrap=WORD, width=55, height=5)
ingredientslist.pack(pady=5)

# Instructions label and Text widget
Label(root, text="Instructions:", font=("Helvetica", 16, "bold"),
      fg="#BA507C", bg="#FFE6EE").pack()
instructions = Text(root, wrap=WORD, width=55, height=10)
instructions.pack(pady=10)

root.mainloop()  # This runs the gui and waits for the user to interact with it
