from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load the Excel data at the start of the application
excel_file_path = 'M10_COF.xlsx'  # Adjust the file path if necessary
excel_data = pd.read_excel(excel_file_path)

# Convert necessary columns to string to ensure consistency
input_columns = [15, 7, 11, 2, 5, 10]  # Column indices for inputs (0-based index)
for col in input_columns:
    excel_data.iloc[:, col] = excel_data.iloc[:, col].astype(str)

@app.route('/')
def index():
    # Prepare options for each column's dropdown (using new column mappings)
    options = {
        'dropdown0': excel_data.iloc[:, 15].dropna().unique().tolist(),  # Column 15
        'dropdown1': excel_data.iloc[:, 7].dropna().unique().tolist(),   # Column 8
        'dropdown2': excel_data.iloc[:, 11].dropna().unique().tolist(),  # Column 12
        'dropdown3': excel_data.iloc[:, 2].dropna().unique().tolist(),   # Column 3
        'dropdown4': excel_data.iloc[:, 5].dropna().unique().tolist(),   # Column 6
        'dropdown5': excel_data.iloc[:, 10].dropna().unique().tolist()   # Column 11
    }
    
    return render_template('index.html', options=options)

@app.route('/search', methods=['GET'])
def search():
    global excel_data

    # Get the selected values for each dropdown
    selected_values = [request.args.get(f'dropdown{i}') for i in range(6)]

    print("Selected Values:", selected_values)  # Debugging print

    # Define column mappings for input and output
    input_columns = [15, 7, 11, 2, 5, 10]  # Column indices for inputs (0-based index)
    output_columns = [19, 34, 35, 36, 29]  # Column indices for outputs (0-based index)

    # Create a list to store the results
    results = []

    # Iterate over each row in the DataFrame
    for _, row in excel_data.iterrows():
        # Check if all selected values match the corresponding columns
        match = True
        for i, value in enumerate(selected_values):
            if value and str(row[input_columns[i]]) != value:
                match = False
                break

        if match:
            # Format the output data from the matched row
            result = {
                'Output1': round(float(row[output_columns[0]]), 2) if pd.notna(row[output_columns[0]]) else 'N/A',
                'Output2': round(float(row[output_columns[1]]), 2) if pd.notna(row[output_columns[1]]) else 'N/A',
                'Output3': round(float(row[output_columns[2]]), 2) if pd.notna(row[output_columns[2]]) else 'N/A',
                'Output4': round(float(row[output_columns[3]]), 2) if pd.notna(row[output_columns[3]]) else 'N/A',
                'Output5': round(float(row[output_columns[4]]), 2) if pd.notna(row[output_columns[4]]) else 'N/A',
            }
            results.append(result)

    print("Results Found:", results)  # Debugging print

    # Return results as JSON
    if results:
        return jsonify({'results': results})
    else:
        return jsonify({'results': 'No matching rows found'})

if __name__ == '__main__':
    app.run(debug=False)
