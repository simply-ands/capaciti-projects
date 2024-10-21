import customtkinter as ctk
import requests
from io import BytesIO
from PIL import Image, ImageTk

# Initialize the app window
app = ctk.CTk()
app.geometry("800x600")
app.title("Text-to-Image Generator")

# Replace with your RapidAPI key and API endpoint
RAPIDAPI_KEY = "927505e68bmshcd72bf19845223cp14312ejsndd09cc108446"
API_URL = "https://chatgpt-vision1.p.rapidapi.com/texttoimageplus"

def generate_image():
    prompt = entry.get()
    payload = {
        "text": prompt,
        "width": 512,
        "height": 512
    }
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "chatgpt-vision1.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        
        data = response.json()
        print(data)  # Print the full response for debugging

        # Extract the image URL from the response
        if 'generated_image' in data:
            image_url = data["generated_image"]
        else:
            raise ValueError("Unexpected response structure")

        # Fetch and display the image in the GUI
        img_data = requests.get(image_url).content
        img = Image.open(BytesIO(img_data))
        img = img.resize((300, 300), Image.LANCZOS)  # Use LANCZOS instead of ANTIALIAS
        tk_img = ImageTk.PhotoImage(img)

        label_image.configure(image=tk_img)
        label_image.image = tk_img  # Keep reference to avoid garbage collection

    except Exception as e:
        label_status.configure(text=f"Error: {e}")
        print(f"Error occurred: {e}")  # Print error to the terminal

# Widgets
entry = ctk.CTkEntry(app, placeholder_text="Enter your prompt here", width=600)
entry.pack(pady=20)

generate_btn = ctk.CTkButton(app, text="Generate Image", command=generate_image)
generate_btn.pack(pady=10)

label_image = ctk.CTkLabel(app, text="")
label_image.pack(pady=20)

label_status = ctk.CTkLabel(app, text="", fg_color="transparent")
label_status.pack(pady=10)

# Run the app
app.mainloop()
