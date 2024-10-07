from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flashing messages

# Default Excel file path
excel_file_path = 'M10_COF.xlsx'

def load_excel_data():
    """Load Excel data and ensure necessary columns are strings."""
    df = pd.read_excel(excel_file_path)
    
    # Define input columns for dropdowns
    dropdown_input_columns = [1, 2, 3, 4, 5, 6]  # Adjust as per your Excel structure
    
    # Define input column for partNo
    partno_input_column = 1  # Adjust to the correct column index for Part No.
    
    # Convert necessary columns to string to ensure consistency
    for col in dropdown_input_columns:
        df.iloc[:, col] = df.iloc[:, col].astype(str)
    
    return df

# Load Excel data initially
excel_data = load_excel_data()

@app.route('/')
def index():
    options = {
        'dropdown0': excel_data.iloc[:, 1].dropna().unique().tolist(),
        'dropdown1': excel_data.iloc[:, 2].dropna().unique().tolist(),
        'dropdown2': excel_data.iloc[:, 3].dropna().unique().tolist(),
        'dropdown3': excel_data.iloc[:, 4].dropna().unique().tolist(),
        'dropdown4': excel_data.iloc[:, 5].dropna().unique().tolist(),
        'dropdown5': excel_data.iloc[:, 6].dropna().unique().tolist()
    }
    return render_template('index.html', options=options)

@app.route('/search', methods=['GET'])
def search():
    global excel_data

    # Check if it's a partNo search
    part_no = request.args.get('partNo')
    if part_no:
        print("Part No Input:", part_no)
        
        # Assuming part number is in column index 1
        input_column_index = 1  # Adjust this index to the correct column for Part No.
        output_columns = [9, 10, 11, 7, 8, 2, 3, 4, 5, 6]  # Column indices for outputs (0-based index)
        
        # Search for matching rows
        results = []
        for _, row in excel_data.iterrows():
            if part_no and str(row.iloc[input_column_index]).strip().lower() == part_no.strip().lower():
                try:
                    # Collecting results without converting to float
                    result = {
                        'Output2': round(float(row.iloc[output_columns[0]]), 2) if pd.notna(row.iloc[output_columns[0]]) else 'N/A',
                        'Output3': round(float(row.iloc[output_columns[1]]), 2) if pd.notna(row.iloc[output_columns[1]]) else 'N/A',
                        'Output4': round(float(row.iloc[output_columns[2]]), 2) if pd.notna(row.iloc[output_columns[2]]) else 'N/A',
                        'Output5': round(float(row.iloc[output_columns[3]]), 2) if pd.notna(row.iloc[output_columns[3]]) else 'N/A',
                        'Output6': round(float(row.iloc[output_columns[4]]), 2) if pd.notna(row.iloc[output_columns[4]]) else 'N/A',
                     #    'Output2': row.iloc[output_columns[0]] if pd.notna(row.iloc[output_columns[0]]) else 'N/A',
                     #   'Output3': row.iloc[output_columns[1]] if pd.notna(row.iloc[output_columns[1]]) else 'N/A',
                     #   'Output4': row.iloc[output_columns[2]] if pd.notna(row.iloc[output_columns[2]]) else 'N/A',
                     #   'Output5': row.iloc[output_columns[3]] if pd.notna(row.iloc[output_columns[3]]) else 'N/A',
                     #   'Output6': row.iloc[output_columns[4]] if pd.notna(row.iloc[output_columns[4]]) else 'N/A',
                        'Output7': row.iloc[output_columns[5]] if pd.notna(row.iloc[output_columns[5]]) else 'N/A',
                        'Output8': row.iloc[output_columns[6]] if pd.notna(row.iloc[output_columns[6]]) else 'N/A',
                        'Output9': row.iloc[output_columns[7]] if pd.notna(row.iloc[output_columns[7]]) else 'N/A',
                        'Output10': row.iloc[output_columns[8]] if pd.notna(row.iloc[output_columns[8]]) else 'N/A',
                        'Output11': row.iloc[output_columns[9]] if pd.notna(row.iloc[output_columns[9]]) else 'N/A',
                    }
                    results.append(result)
                except Exception as e:
                    print(f"Error processing result: {e}")
        
        print("Results Found (partNo):", results)
        if results:
            return jsonify({'results': results})
        else:
            return jsonify({'results': 'No matching rows found'})
    
    # Else, assume it's a dropdown search
    selected_values = [request.args.get(f'dropdown{i}') for i in range(6)]
    print("Selected Values:", selected_values)
    
    # Define input and output columns for dropdown search
    dropdown_input_columns = [6, 3, 4, 5, 2]  # Adjust based on your Excel structure
    output_columns = [8, 9, 10, 11, 7, 1]  # Adjust based on your Excel structure
    
    results = []
    for _, row in excel_data.iterrows():
        match = True
        for i, value in enumerate(selected_values):
            if value and str(row.iloc[dropdown_input_columns[i]]).strip().lower() != value.strip().lower():
                match = False
                break

        if match:
            result = {
                'Output1': round(float(row.iloc[output_columns[0]]), 2) if pd.notna(row.iloc[output_columns[0]]) else 'N/A',
                'Output2': round(float(row.iloc[output_columns[1]]), 2) if pd.notna(row.iloc[output_columns[1]]) else 'N/A',
                'Output3': round(float(row.iloc[output_columns[2]]), 2) if pd.notna(row.iloc[output_columns[2]]) else 'N/A',
                'Output4': round(float(row.iloc[output_columns[3]]), 2) if pd.notna(row.iloc[output_columns[3]]) else 'N/A',
                'Output5': round(float(row.iloc[output_columns[4]]), 2) if pd.notna(row.iloc[output_columns[4]]) else 'N/A',
                'Output6': row.iloc[output_columns[5]] if pd.notna(row.iloc[output_columns[5]]) else 'N/A',
            }
            results.append(result)

    print("Results Found (dropdown):", results)
    if results:
        return jsonify({'results': results})
    else:
        return jsonify({'results': 'No matching rows found'})

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    global excel_file_path, excel_data
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            
            if file and file.filename.endswith('.xlsx'):
                # Save the uploaded file with the same name as the existing file
                file.save(excel_file_path)
                
                # Load the new Excel data from the updated file
                excel_data = load_excel_data()

                flash('File uploaded and data updated successfully')
                return redirect(url_for('index'))
            else:
                flash('Invalid file type. Only .xlsx files are allowed.')
                return redirect(request.url)

        except Exception as e:
            print(f"Error: {e}")  # Print the error to the console for debugging
            flash('An error occurred while processing the file.')
            return redirect(request.url)

    return render_template('admin.html')

@app.route('/index1')
def index1():
    options = {
        'dropdown0': excel_data.iloc[:, 6].dropna().unique().tolist(),
        'dropdown1': excel_data.iloc[:, 3].dropna().unique().tolist(),
        'dropdown2': excel_data.iloc[:, 4].dropna().unique().tolist(),
        'dropdown3': excel_data.iloc[:, 5].dropna().unique().tolist(),
        'dropdown4': excel_data.iloc[:, 2].dropna().unique().tolist(),
    }
    return render_template('index1.html', options=options)

@app.route('/index2')
def index2():
    return render_template('index2.html')

if __name__ == '__main__':
    app.run(debug=False)
