# Bolt-Coefficient
# VECV Bolt Coefficient of Friction Library

This project is a Flask-based web application designed to manage and search through an Excel file (`M10_COF.xlsx`) and display data based on part number input or dropdown selections.

## Features
- Upload Excel files via the admin panel
- Search for part numbers and return relevant data
- Dropdown-based searches with multiple criteria

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.x
- Pip (Python package manager)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo-url.git
    ```

2. Change into the project directory:
    ```bash
    cd your-project-directory
    ```

3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Ensure your Excel file `M10_COF.xlsx` is placed in the project root directory.

## Running the Application

1. Run the Flask app:
    ```bash
    python app.py
    ```

2. Open a browser and navigate to:
    ```
    http://127.0.0.1:5000/
    ```

3. Admin panel for uploading Excel files:
    ```
    http://127.0.0.1:5000/admin
    ```

## Deployment

For deployment, follow the specific instructions for the platform you're using (Heroku, AWS, Remedy, etc.). In most cases, ensure you have the following files:

- `Procfile` (for platforms like Heroku):
    ```
    web: python app.py
    ```

- `requirements.txt`: Make sure all the dependencies are listed here.
