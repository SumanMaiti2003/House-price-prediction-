from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import pickle

app = Flask(__name__)

# Load the dataset and model
data = pd.read_csv('final_dataset.csv')
pipe = pickle.load(open('RidgeModel.pkl', 'rb'))  # Load the trained model

@app.route('/')
def index():
    # Prepare dropdown values
    bedrooms = sorted(data['beds'].dropna().unique())
    bathrooms = sorted(data['baths'].dropna().unique())
    sizes = sorted(data['size'].dropna().unique())
    zip_codes = sorted(data['zip_code'].dropna().unique())

    return render_template('index.html', bedrooms=bedrooms, bathrooms=bathrooms, sizes=sizes, zip_codes=zip_codes, prediction=None)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get user inputs
        bedrooms = int(float(request.form.get("beds")))
        bathrooms = int(float(request.form.get("baths")))
        size = int(float(request.form.get("size")))
        zip_code = int(float(request.form.get("zip_code")))

        # Create input DataFrame
        input_data = pd.DataFrame([[bedrooms, bathrooms, size, zip_code]], columns=['beds', 'baths', 'size', 'zip_code'])

        # Handle unknown categories
        for column in input_data.columns:
            if input_data[column].iloc[0] not in data[column].unique():
                input_data[column] = data[column].mode()[0]

        # Make prediction
        prediction = pipe.predict(input_data)[0]
        prediction = np.round(prediction, 2)

        # Reload page with dropdowns + prediction
        bedrooms = sorted(data['beds'].dropna().unique())
        bathrooms = sorted(data['baths'].dropna().unique())
        sizes = sorted(data['size'].dropna().unique())
        zip_codes = sorted(data['zip_code'].dropna().unique())

        return render_template('index.html', bedrooms=bedrooms, bathrooms=bathrooms, sizes=sizes, zip_codes=zip_codes, prediction=prediction)

    except Exception as e:
        return f"Error occurred: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
