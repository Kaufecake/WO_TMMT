# Wurm Online Treasure Map Mapping Tool Project

## Authors
The original contributing authors are Kaufecake and Liah, both are located on the Cadence server of the Northern Freedom Isles Cluster.
Liah is primarily responsible for the Google Sheets processing portion of this project.
Kaufecake is primarily responsible for the Python portion of this project.

## Background
This project is designed to dynamically plot coordinates from the TMMT Google Sheets spreadsheet onto a specific server's map, based on user selections. The map and its scale are set by the server type, allowing users to visualize map locations.

The program connects to a Google Sheets document, where data is managed and parsed, and to a CSV file that provides server-specific settings. These include an image link for each map and a scaling factor to accommodate varying map sizes.

### Features
- Dynamic selection of server maps
- Automatic parsing of Yaga map links
- Filtered display for unfinished maps
- Adjustable plot scaling

### Revision History
- **v0.1** Initial setup and basic functionality
  - Hosted solely in Google Sheets
  - Minimal functionality, and limited applicability (Cadence only)
  - Plotted data points with nnumber annotations on Cadence

- **v0.2** Split Functionality Between Github and Google Sheets
  - Created basic GUI for server selection
  - Integrated all maps for server image links and scaling factors
  - Implemented error handling for unexpected Google Sheets data


### Future Goals
- Bugfix
- Implement features as requested

---
