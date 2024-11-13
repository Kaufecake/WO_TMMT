import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import matplotlib.pyplot as plt
from PIL import Image
import tkinter as tk
from tkinter import simpledialog

# Set Up Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets"]
creds = ServiceAccountCredentials.from_json_keyfile_name("path/to/credentials.json", scope)
client = gspread.authorize(creds)

# Function to get data from the main Google Sheet with validation
def get_data_from_google_sheet(sheet_id):
    sheet = client.open_by_key(sheet_id).sheet1
    data = sheet.get_all_records()

    # Check data format
    expected_keys = {"Map Name", "Map Link", "Completed"}
    for row in data:
        if not expected_keys.issubset(row.keys()):
            print("Unexpected data in spreadsheet.")
            return None  # Cease further processing
    return data

# Function to read server settings from a Google Sheet, "Map_Matrix" tab
def load_server_settings(sheet_id):
    sheet = client.open_by_key(sheet_id).worksheet("Map_Matrix")
    data = sheet.get_all_records()

    server_settings = {}
    for row in data:
        server_name = row['Server'].capitalize()
        image_link = row['Image Link']
        x_dim = float(row['X Dim'])
        y_dim = float(row['Y Dim'])
        server_settings[server_name] = {
            "image_link": image_link,
            "x_dim": x_dim,
            "y_dim": y_dim
        }
    return server_settings

# Function to parse 'Map Link' and add 'Server', 'X Coord', 'Y Coord'
def parse_map_link(data):
    parsed_data = []
    for row in data:
        map_name = row['Map Name']
        map_link = row['Map Link']
        finished = row['Completed']

        # Extract the Server, X Coord, and Y Coord from 'Map Link'
        server_match = re.search(r"https://(.*?).yaga.host", map_link)
        coord_match = re.search(r"yaga.host/#(\d+),(\d+)", map_link)

        server = server_match.group(1).capitalize() if server_match else None
        x_coord = int(coord_match.group(1)) if coord_match else None
        y_coord = int(coord_match.group(2)) if coord_match else None

        # Add parsed data to new array
        parsed_data.append([map_name, server, x_coord, y_coord, finished])
    return parsed_data

# Function to filter data based on server and completion status
def filter_data(data, selected_server, show_finished=False):
    filtered_data = [
        row for row in data
        if row[1] == selected_server and (show_finished or row[4].lower() == "false")
    ]
    return filtered_data

# Function to plot the coordinates with bubbles and name annotations
def plot_coordinates(data, background_image_path, x_dim, y_dim, zoom_factor=1.0):
    img = plt.imread(background_image_path)
    fig, ax = plt.subplots()

    # Scale and zoom configurations
    ax.imshow(img, extent=[0, x_dim, 0, y_dim])
    ax.set_xlim([0, x_dim * zoom_factor])
    ax.set_ylim([0, y_dim * zoom_factor])

    # Plot data points with bubbles and name annotations
    for row in data:
        x, y, name = row[2], row[3], row[0]
        plt.scatter(x, y, color='blue', alpha=0.5)  # Plot bubbles at coordinates
        plt.text(x + 5, y + 5, name, fontsize=8, color='black', alpha=0.8)  # Name label

    plt.show()

# GUI for server selection and Google Sheet URL input
def gui_for_server_and_sheet_input():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Prompt for Google Sheet link
    sheet_url = simpledialog.askstring("Google Sheet Link", "Enter the link to your Google Sheet with the map data:")
    # Extract the sheet ID from the URL
    sheet_id = sheet_url.split("/d/")[1].split("/")[0] if "/d/" in sheet_url else None

    # Ask for server selection
    server_options = [
        "Independence", "Deliverance", "Exodus", "Celebration", "Pristine", 
        "Release", "Xanadu", "Chaos", "Elevation", "Desertion", "Affliction", 
        "Serenity", "Harmony", "Melody", "Cadence", "Defiance"
    ]
    selected_server = simpledialog.askstring("Select Server", f"Choose a server from: {', '.join(server_options)}")

    return sheet_id, selected_server

# Main script to integrate all functions
def main():
    # Prompt user for Google Sheet URL and server selection
    sheet_id, selected_server = gui_for_server_and_sheet_input()
    
    if not sheet_id:
        print("Invalid Google Sheet link. Exiting program.")
        return  # Stop if the sheet link is invalid

    # Load server settings from the provided Google Sheet's "Map_Matrix" tab
    server_settings = load_server_settings(sheet_id)

    # Step 1: Get data from the primary Google Sheet
    raw_data = get_data_from_google_sheet(sheet_id)
    
    if raw_data is None:
        return  # Stop if there's unexpected data

    # Step 2: Parse data
    parsed_data = parse_map_link(raw_data)

    # Step 3: Filter data based on server and completion status
    filtered_data = filter_data(parsed_data, selected_server)

    # Step 4: Plot filtered data using the selected server's settings
    if selected_server in server_settings:
        server_info = server_settings[selected_server]
        plot_coordinates(
            filtered_data,
            background_image_path=server_info["image_link"],
            x_dim=server_info["x_dim"],
            y_dim=server_info["y_dim"]
        )
    else:
        print("Selected server does not have corresponding settings in the Google Sheet.")

if __name__ == "__main__":
    main()
