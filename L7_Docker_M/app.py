from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Functie pentru a verifica daca prima coloana contine 'id' (case-insensitive)
def is_id_column(column_name):
    return any(keyword in column_name.lower() for keyword in ['id'])

@app.route('/')
def upload_file():
    return render_template('index.html')

# Ruta pentru procesarea fisierului CSV
@app.route('/procesare', methods=['POST'])
def procesare_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'Nu s-a incarcat nici un fisier'}), 400
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'Nu ai selectat nici un fisier CSV'}), 400

    if file and file.filename.endswith('.csv'):
        # Citirea fisierului CSV in Pandas DataFrame
        df = pd.read_csv(file, sep=';')

        # Excluderea primei coloane din procesare dacă reprezintă ID-uri
        # df = df.iloc[:, 1:] # Exclude prima coloana
        if is_id_column(df.columns[0]):
            df = df.drop(df.columns[0], axis=1)

        # Dictionar pentru a stoca valorile unice si numarul lor de aparitii
        unique_values_counts = {}

        # Itereaza prin fiecare coloana din DataFrame si aplica value_counts()
        for column in df.columns:
            unique_values_counts[column] = df[column].value_counts().to_dict()

        # Crearea unui rezultat cu numarul de randuri si valorile unice pentru fiecare coloana
        summary = {
            'num_rows': len(df),
            'columns': list(df.columns),
            'unique_values_counts': unique_values_counts
        }

        return jsonify(summary)
    
    return jsonify({'error': 'Fisier neacceptat, incarca un fisier CSV.'}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)