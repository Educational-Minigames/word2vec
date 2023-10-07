color_list = [
    "rgb(255, 0, 0)",    # Red
    "rgb(0, 255, 0)",    # Green
    "rgb(0, 0, 255)",    # Blue
    "rgb(255, 255, 0)",  # Yellow
    "rgb(255, 0, 255)",  # Magenta
    "rgb(0, 255, 255)",  # Cyan
    "rgb(255, 128, 0)",  # Orange
    "rgb(128, 0, 255)",  # Purple
    "rgb(0, 255, 128)",  # Teal
    "rgb(128, 255, 0)",  # Lime
    "rgb(255, 0, 128)",  # Pink
    "rgb(0, 128, 255)",  # Sky Blue
    "rgb(255, 128, 128)",# Light Red
    "rgb(128, 255, 128)",# Light Green
    "rgb(128, 128, 255)",# Light Blue
    "rgb(255, 255, 128)",# Light Yellow
    "rgb(255, 128, 255)",# Light Magenta
    "rgb(128, 255, 255)",# Light Cyan
    "rgb(255, 192, 128)",# Peach
    "rgb(192, 255, 128)" # Light Lime
]
def map_strings_to_colors(string_list):
    unique_strings = sorted(list(set(string_list)))  # Get unique strings
    color_mapping = {}

    # Generate a unique color for each string
    for i, unique_str in enumerate(unique_strings):
        color_mapping[unique_str] = color_list[i]

    # Map the strings to colors
    result = [color_mapping[string] for string in string_list]

    return result