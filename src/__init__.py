from datetime import datetime, timedelta

from PIL import Image


def make_color_transparent(input_path, output_path, target_color_hex):
    # Convert hexadecimal color code to RGB tuple
    target_color = tuple(int(target_color_hex[i : i + 2], 16) for i in (1, 3, 5))

    # Open the image
    image = Image.open(input_path)

    # Convert the image to RGBA (if not already in that mode)
    image = image.convert("RGBA")

    # Get the image data as a list of tuples
    data = list(image.getdata())

    # Create a new list to store the modified data
    new_data = []

    # Define a function to check if a pixel matches the target color
    def is_target_color(pixel):
        return pixel[:3] == target_color

    # Iterate through the image data and make the target color transparent
    for pixel in data:
        if is_target_color(pixel):
            # Make the target color transparent (set alpha to 0)
            new_data.append((0, 0, 0, 0))
        else:
            new_data.append(pixel)

    # Create a new image with the modified data
    new_image = Image.new("RGBA", image.size)
    new_image.putdata(new_data)

    # Save the image with transparency as a PNG
    new_image.save(output_path, format="PNG")


def create_week(weekday):
    en_2_kr = {
        "Monday": "mon",
        "Tuesday": "tue",
        "Wednesday": "wed",
        "Thursday": "thu",
        "Friday": "fri",
        "Saturday": "sat",
        "Sunday": "sun",
    }
    new_weekdays = []
    for week in weekday:
        new_weekdays.append(en_2_kr[week])

    return new_weekdays


def create_date_string(first_date: datetime):
    dates = [first_date + timedelta(days=i) for i in range(7)]
    return [date.strftime("%m.%d") for date in dates]


def eng_week_2_korean_week(weeks):
    kr_2_eng = {
        "mon": "월",
        "tue": "화",
        "wed": "수",
        "thu": "목",
        "fri": "금",
        "sat": "토",
        "sun": "일",
    }

    eng_weeks = [kr_2_eng[week] for week in weeks]

    return eng_weeks
