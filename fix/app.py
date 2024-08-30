from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load the Excel data at the start of the application
excel_file_path = 'M10_COF.xlsx'  # Adjust the file path if necessary
excel_data = pd.read_excel(excel_file_path)

@app.route('/')
def index():
    # Prepare options for each column's dropdown (assuming the first 6 columns)
    options = {f'dropdown{i}': excel_data.iloc[:, i].dropna().unique().tolist() for i in range(6)}
    
    return render_template('index.html', options=options)

@app.route('/search')
def search():
    global excel_data

    # Get the selected values for each dropdown
    selected_values = [request.args.get(f'dropdown{i}') for i in range(6)]

    # Ensure that the Excel data is available and all values are selected
    if not all(selected_values):
        return jsonify({'results': 'Invalid input or data not available'})

    # Filter the DataFrame based on the selected values
    filter_condition = pd.Series([True] * len(excel_data))
    for i, value in enumerate(selected_values):
        filter_condition &= (excel_data.iloc[:, i] == value)

    filtered_data = excel_data[filter_condition]

    # If any matching rows are found, return the next five columns for each match
    if not filtered_data.empty:
        results = []
        start_col = 6  # Since we're matching based on the first 6 columns
        end_col = start_col + 5  # Get the next 5 columns
        
        for _, matched_row in filtered_data.iterrows():
            result = matched_row.iloc[start_col:end_col].to_dict()
            results.append(result)

        return jsonify({'results': results})
    else:
        return jsonify({'results': 'No matching row found'})

if __name__ == '__main__':
    app.run(debug=True)
