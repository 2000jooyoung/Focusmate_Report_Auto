from PIL import Image

def resize_image(input_path, output_path, new_size):
    try:
        # Open the image file
        with Image.open(input_path) as img:
            # Resize the image
            resized_img = img.resize(new_size)

            # Save the resized image
            resized_img.save(output_path)

        print(f"Image resized and saved to {output_path}")

    except Exception as e:
        print(f"Error: {e}")