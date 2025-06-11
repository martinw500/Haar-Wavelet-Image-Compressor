import customtkinter as ctk
from PIL import Image, ImageTk
import numpy as np
from tkinter import filedialog

# Initialize customtkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Variables to hold image data
image_array = None
original_image = None  # To store the original image
processed_image = None  # To store the processed image
ny, nx = 0, 0
max_image_size = 300  # Maximum width/height for displayed images

# Initialize threshold and iteration variables
threshold_value = 0
iteration_value = 0

# Haar Wavelet functions for compressing image
def H(image_array, iteration):
    for row in range(ny):
        for i in range(iteration):
            rowCopy = image_array[row].copy()
            compresslength = nx // (2**(i+1))
            for j in range(compresslength):
                average = (image_array[row, 2*j] + image_array[row, 2*j+1]) / 2
                difference = (image_array[row, 2*j] - average)
                rowCopy[j] = average
                rowCopy[compresslength + j] = difference
            image_array[row] = rowCopy.copy()
    return image_array

def Hinv(image_array, iteration):
    for row in range(ny):
        for i in range(iteration - 1, -1, -1):
            rowCopy = image_array[row].copy()
            compresslength = nx // (2**(i+1))
            for j in range(compresslength):
                average = rowCopy[j]
                difference = rowCopy[compresslength + j]
                image_array[row, 2*j] = average + difference
                image_array[row, 2*j+1] = average - difference
    return image_array

def HT(image_array, iteration):
    for col in range(nx):
        for i in range(iteration):
            colCopy = image_array[:, col].copy()
            compresslength = ny // (2**(i+1))
            for j in range(compresslength):
                average = (image_array[2*j, col] + image_array[2*j+1, col]) / 2
                difference = (image_array[2*j, col] - average)
                colCopy[j] = average
                colCopy[compresslength + j] = difference
            image_array[:, col] = colCopy.copy()
    return image_array

def HTinv(image_array, iteration):
    for col in range(nx):
        for i in range(iteration - 1, -1, -1):
            colCopy = image_array[:, col].copy()
            compresslength = ny // (2**(i+1))
            for j in range(compresslength):
                average = colCopy[j]
                difference = colCopy[compresslength + j]
                image_array[2*j, col] = average + difference
                image_array[2*j+1, col] = average - difference
    return image_array

# Load and process image
def load_image():
    global image_array, original_image, ny, nx
    file_path = filedialog.askopenfilename(title="Select an Image File", filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if not file_path:
        print("No file selected.")
        return

    # Load the image in RGB
    image = Image.open(file_path).convert('RGB')
    image_array = np.asarray(image, dtype=np.float32)
    ny, nx, _ = image_array.shape  # Get the dimensions (height, width, channels)
    original_image = image  # Keep the original color image for display
    display_image(original_image, original_canvas)

def process_image():
    global processed_image
    if image_array is None:
        print("No image loaded.")
        return

    # Use the slider values
    threshold = threshold_slider.get()
    iterations = iteration_slider.get()

    print(f"Processing with threshold: {threshold}, iterations: {iterations}")

    # Split into R, G, B channels
    red, green, blue = image_array[:, :, 0], image_array[:, :, 1], image_array[:, :, 2]

    # Process each channel individually
    for channel in [red, green, blue]:
        transformed = H(channel.copy(), iteration=int(iterations))
        transformed = HT(transformed, iteration=int(iterations))
        transformed[np.abs(transformed) < threshold] = 0
        reconstructed = HTinv(transformed.copy(), iteration=int(iterations))
        reconstructed = Hinv(reconstructed, iteration=int(iterations))
        channel[:, :] = np.clip(reconstructed, 0, 255)

    # Combine the processed channels back into an RGB image
    reconstructed_image = np.stack((red, green, blue), axis=-1).astype(np.uint8)
    processed_image = Image.fromarray(reconstructed_image)
    display_image(processed_image, processed_canvas)

def display_image(image, canvas):
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    # Resize the image to fit the canvas
    width, height = image.size
    scale = min(canvas_width / width, canvas_height / height)
    new_size = (int(width * scale), int(height * scale))
    resized_image = image.resize(new_size, Image.Resampling.LANCZOS)

    img = ImageTk.PhotoImage(resized_image)

    # Clear previous canvas content
    canvas.delete("all")

    # Display the image on the canvas, centering it
    canvas.create_image(canvas_width / 2, canvas_height / 2, anchor="center", image=img)
    canvas.image = img  # Keep a reference to avoid garbage collection

def resize_canvas(event):
    # Update both original and processed canvases on window resize
    if original_image:
        display_image(original_image, original_canvas)
    if processed_image:
        display_image(processed_image, processed_canvas)

# GUI setup (same as before)
app = ctk.CTk()
app.geometry("800x500")
app.title("Color Image Compression Tool")

frame = ctk.CTkFrame(app)
frame.pack(pady=20, padx=20, fill="both", expand=True)

button_frame = ctk.CTkFrame(frame)
button_frame.pack(side="top", fill="x", pady=10)

load_button = ctk.CTkButton(button_frame, text="Load Image", command=load_image)
load_button.pack(side="left", padx=10)

process_button = ctk.CTkButton(button_frame, text="Process Image", command=process_image)
process_button.pack(side="left", padx=10)

image_frame = ctk.CTkFrame(frame)
image_frame.pack(fill="both", expand=True, padx=10, pady=10)

original_canvas = ctk.CTkCanvas(image_frame, bg="gray")
original_canvas.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
ctk.CTkLabel(image_frame, text="Original Image").grid(row=1, column=0, pady=5)

processed_canvas = ctk.CTkCanvas(image_frame, bg="gray")
processed_canvas.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")
ctk.CTkLabel(image_frame, text="Processed Image").grid(row=1, column=1, pady=5)

image_frame.grid_rowconfigure(0, weight=1)
image_frame.grid_columnconfigure(0, weight=1)
image_frame.grid_columnconfigure(1, weight=1)

slider_frame = ctk.CTkFrame(frame)
slider_frame.pack(side="bottom", fill="x", pady=10)

ctk.CTkLabel(slider_frame, text="Threshold:").pack(side="left", padx=10)
threshold_slider = ctk.CTkSlider(slider_frame, from_=0, to=5, number_of_steps=5)
threshold_slider.pack(side="left", padx=10)

ctk.CTkLabel(slider_frame, text="Iterations:").pack(side="left", padx=10)
iteration_slider = ctk.CTkSlider(slider_frame, from_=0, to=5, number_of_steps=5)
iteration_slider.pack(side="left", padx=10)

app.bind("<Configure>", resize_canvas)

app.mainloop()