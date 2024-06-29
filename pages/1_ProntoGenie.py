import streamlit as st
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
import numpy as np
import warnings
import os
import time
import datetime
import matplotlib.pyplot as plt

# Suppress warnings
warnings.filterwarnings('ignore')

# Sidebar layout including logo
st.sidebar.image('assets/logo_1_1.png', width=250)  # Adjust path and width as needed
st.sidebar.title("Upload Documents Data File")
data_1_file = st.sidebar.file_uploader("Upload File", type=["xlsx"])

# Display green box to upload file
if data_1_file is None:
    st.sidebar.info("🟢 Upload a file to get started!")

# Add a link to view the format with an image
with st.sidebar.expander("View data format"):
    st.image('assets/excelformat.png', use_column_width=True)  # Path to your image in the assets folder

@st.cache_data
def load_data(data_1_file):
    data_1 = pd.read_excel(data_1_file)
    return data_1

@st.cache_data
def preprocess_data(data_1):
    # Ensure required columns are present
    required_columns = ['createdOn', 'jobcode', 'module']
    missing_columns = [col for col in required_columns if col not in data_1.columns]
    if missing_columns:
        st.error(f"Uploaded file is missing the following required columns: {', '.join(missing_columns)}")
        return None

    # Convert 'createdOn' to datetime
    data_1['createdOn'] = pd.to_datetime(data_1['createdOn'], errors='coerce')
    data_1 = data_1.dropna(subset=['createdOn'])  # Drop rows with invalid dates

    # Ensure 'jobcode' and 'module' are treated as strings
    data_1['jobcode'] = data_1['jobcode'].astype(str)
    data_1['module'] = data_1['module'].astype(str)

    return data_1

@st.cache_data
def process_and_train(data_1):
    # Convert columns to datetime
    data_1['createdOn'] = pd.to_datetime(data_1['createdOn'])

    # Extract day, month, year, and day of the week from 'createdOn' in data_1
    data_1['day'] = data_1['createdOn'].dt.day
    data_1['month'] = data_1['createdOn'].dt.month
    data_1['year'] = data_1['createdOn'].dt.year
    data_1['day_of_week'] = data_1['createdOn'].dt.dayofweek

    # Calculate the number of projects (unique job codes) for each month and year
    projects_data = data_1.groupby(['year', 'month'])['jobcode'].nunique().reset_index(name='No of Projects')

    # Group by day, month, year, day_of_week, module to get the count of documents received
    document_counts = data_1.groupby(['day', 'month', 'year', 'day_of_week', 'module']).size().reset_index(name='count')

    # Merge with projects data to get the number of projects for each month and year
    merged_data = document_counts.merge(projects_data, how='left', left_on=['month', 'year'], right_on=['month', 'year'])

    # Fill missing values in 'No of Projects' with 0 (if any)
    merged_data['No of Projects'] = merged_data['No of Projects'].fillna(0)

    # Function to train a model for a specific document type
    def train_model_for_module(module):
        module_data = merged_data[merged_data['module'] == module]

        # Define features and target variable
        categorical_features = ['day', 'month', 'year', 'day_of_week']
        X = module_data[categorical_features + ['No of Projects']]
        y_target = module_data['count']

        # One-hot encode the categorical variables
        encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        encoded_columns = encoder.fit_transform(module_data[categorical_features])
        encoded_columns_df = pd.DataFrame(encoded_columns, columns=encoder.get_feature_names_out(categorical_features))

        # Prepare the transformer and pipeline
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', encoder, categorical_features)
            ],
            remainder='passthrough'
        )

        # Use cross-validation to find the best degree for the polynomial features
        best_degree = 1
        best_score = float('-inf')

        for degree in range(1, 4):  # Test polynomial degrees from 1 to 3
            model = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('poly', PolynomialFeatures(degree=degree, include_bias=False)),
                ('regressor', Ridge(alpha=1.0))  # Regularization parameter alpha can be tuned
            ])

            scores = cross_val_score(model, X, y_target, cv=5, scoring='neg_mean_squared_error')
            mean_score = np.mean(scores)

            if mean_score > best_score:
                best_score = mean_score
                best_degree = degree

        # Use the best degree for the final model
        model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('poly', PolynomialFeatures(degree=best_degree, include_bias=False)),
            ('regressor', Ridge(alpha=1.0))
        ])

        # Fit the model
        model.fit(X, y_target)
        return model

    # Train models for each document type
    modules = merged_data['module'].unique()
    models = {module: train_model_for_module(module) for module in modules}

    return models, modules, projects_data

# Function to predict documents for a given month and year
def predict_documents(year, month, no_of_projects, models, modules, selected_module=None):
    try:
        # Generate dates for the entire month
        dates = pd.date_range(start=f'{year}-{month:02d}-01', end=f'{year}-{month:02d}-{pd.Timestamp(year, month, 1).days_in_month}')
        predictions = []

        for date in dates:
            day = date.day
            day_of_week = date.dayofweek
            if selected_module and selected_module != "All":
                data = pd.DataFrame({
                    'module': [selected_module],
                    'day': [day],
                    'month': [month],
                    'year': [year],
                    'day_of_week': [day_of_week],
                    'No of Projects': [no_of_projects]
                })
                prediction = models[selected_module].predict(data[['day', 'month', 'year', 'day_of_week', 'No of Projects']])
                prediction = np.ceil(np.clip(prediction, 0, None))
                predictions.append([date.strftime('%Y-%m-%d'), prediction[0], prediction[0]])
            else:
                data = pd.DataFrame({
                    'module': modules,
                    'day': [day] * len(modules),
                    'month': [month] * len(modules),
                    'year': [year] * len(modules),
                    'day_of_week': [day_of_week] * len(modules),
                    'No of Projects': [no_of_projects] * len(modules)
                })
                prediction = [models[module].predict(data[['day', 'month', 'year', 'day_of_week', 'No of Projects']][data['module'] == module])[0] for module in modules]
                prediction = np.ceil(np.clip(prediction, 0, None))
                total_documents = np.sum(prediction)
                predictions.append([date.strftime('%Y-%m-%d')] + list(prediction) + [total_documents])

        # Create the dataframe
        columns = ['Date'] + (['count', 'Total Documents'] if selected_module and selected_module != "All" else list(modules) + ['Total Documents'])
        predictions_df = pd.DataFrame(predictions, columns=columns)

        # Calculate column-wise total
        totals = predictions_df.drop('Date', axis=1).sum(axis=0)
        totals['Date'] = 'Total'
        totals = pd.DataFrame(totals).T
        predictions_df = pd.concat([predictions_df, totals], ignore_index=True)

        return predictions_df

    except Exception as e:
        st.error(f"Error during document prediction: {e}")

# Function to predict future documents based on input parameters
def predict_future_docs(num_projects_next_month, start_date, months, models, modules, selected_module=None):
    try:
        start_date_obj = pd.to_datetime(start_date)
        predictions = []

        for i in range(months):
            year = start_date_obj.year
            month = start_date_obj.month
            predictions_df = predict_documents(year, month, num_projects_next_month, models, modules, selected_module)
            predictions_df['Month'] = pd.to_datetime(f"{year}-{month}-01").strftime('%B')
            predictions.append(predictions_df)
            start_date_obj = start_date_obj + pd.DateOffset(months=1)

        return pd.concat(predictions, ignore_index=True)

    except Exception as e:
        st.error(f"Error during future document prediction: {e}")
        
# Main Streamlit application
def main():
    # Title and tagline for Pronto Mitra
    col1, col2 = st.columns([6, 1])
    with col2:
        st.image('assets/ProntoGenie.png', use_column_width=True)  # Path to your image in the assets folder
    with col1:
        st.title("Welcome to Pronto Mitra")
        st.write("## Pronto Genie")


    # Wait for file uploads
    if data_1_file:
        try:
            data_1 = load_data(data_1_file)
            data_1 = preprocess_data(data_1)
            if data_1 is None:
                return

            # Convert the 'createdOn' column to datetime
            data_1['createdOn'] = pd.to_datetime(data_1['createdOn'], errors='coerce')

            # Extract year and month from 'createdOn' column in data_1
            data_1['year'] = data_1['createdOn'].dt.year
            data_1['month'] = data_1['createdOn'].dt.month
            
            with st.spinner('Processing....'):
                models, modules, projects_data = process_and_train(data_1)
                if models is None or modules is None:
                    return

            # Calculate the number of documents for each month and year
            document_counts = data_1.groupby(['year', 'month']).size().reset_index(name='No of Documents')

            # Merge with projects data to get the number of documents for each month and year
            projects_data = projects_data.merge(document_counts, how='left', on=['year', 'month'])

            # Convert year and month to string to avoid displaying with commas
            projects_data['year'] = projects_data['year'].astype(str)
            projects_data['month'] = projects_data['month'].apply(lambda x: pd.to_datetime(f'2024-{x}-01').strftime('%B'))

            # Display the number of projects for each month
            st.subheader("Summary")
            st.write(projects_data, index=False)  # Display without index
            
            # Calculate and display the total number of documents
            total_documents = projects_data['No of Documents'].sum()
            st.write(f"**Total number of documents till date: {total_documents}**")
            
            
            st.markdown("<br>", unsafe_allow_html=True)  # This adds a line break

            # Sidebar for additional inputs
            st.sidebar.title("Prediction Parameters")
            current_year = datetime.datetime.now().year
            months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
            years = list(range(2021, 2150))  # Adjust the range of years as needed

            selected_month = st.sidebar.selectbox("Select Month", options=months, index=5)  # Default to June
            selected_year = st.sidebar.selectbox("Select Year", options=years, index=years.index(current_year))

            # Convert selected month and year to a datetime object
            start_date = pd.to_datetime(f"{selected_year}-{months.index(selected_month) + 1:02d}-01")
            
            months_to_predict = st.sidebar.number_input("Number of Months to Predict", min_value=1, value=1)
            selected_module = st.sidebar.selectbox("Select Module", options=["All"] + list(modules))

            # Input fields for number of projects for each month
            projects_per_month = {}
            for i in range(months_to_predict):
                month_name = (start_date + pd.DateOffset(months=i)).strftime('%B')
                projects_per_month[month_name] = st.sidebar.number_input(f"Number of Projects for {month_name}", min_value=1, value=130)

            if st.sidebar.button("Predict"):
                
                
                all_predictions = {}  # Dictionary to hold all predictions
                with st.spinner('Running predict_future_docs...'):
                    for i in range(months_to_predict):
                        # Calculate the prediction month
                        prediction_month = start_date + pd.DateOffset(months=i)
                        prediction_month_year = prediction_month.year
                        prediction_month_number = prediction_month.month
                        
                        # Get number of projects for the current month
                        num_projects_next_month = projects_per_month[prediction_month.strftime('%B')]

                        # Get predictions for the current month
                        predictions_df = predict_documents(prediction_month_year, prediction_month_number, num_projects_next_month, models, modules, selected_module)
                        
                        # Store predictions in the dictionary
                        sheet_name = f"{prediction_month.strftime('%B_%Y')}"
                        all_predictions[sheet_name] = predictions_df
                        
                        # Display predictions table for the current month
                        st.subheader(f'Predicted Documents Count for {prediction_month.strftime("%B %Y")}')
                        st.write(predictions_df, index=False)  # Display without index

                        # Plotting the graph for the current month
                        st.subheader(f'Predicted Documents Graph for {prediction_month.strftime("%B %Y")}')
                        fig, ax = plt.subplots(figsize=(10, 6))
                        predictions_df.set_index('Date', inplace=True)

                        # Extracting day numbers for the x-axis
                        day_numbers = [pd.to_datetime(date).day for date in predictions_df.index if date != 'Total']
                        # Plotting the data
                        if selected_module and selected_module != "All":
                            ax.plot(day_numbers, predictions_df.loc[predictions_df.index != 'Total', 'count'], label=selected_module)
                        else:
                            for module in modules:
                                ax.plot(day_numbers, predictions_df.loc[predictions_df.index != 'Total', module], label=module)
                        ax.set_xlabel('Day of the Month')
                        ax.set_ylabel('Document Count')
                        ax.set_title(f'Predicted Daywise Documents (Module Wise) for {prediction_month.strftime("%B %Y")}')
                        ax.legend()
                        ax.grid(True)
                        # Setting the x-axis ticks to show only day numbers
                        ax.set_xticks(day_numbers)
                        ax.set_xticklabels(day_numbers)
                        st.pyplot(fig)

                # Save all predictions to a single Excel file with separate sheets
                combined_output_filename = f'all_predictions_{start_date.strftime("%B_%Y")}_to_{(start_date + pd.DateOffset(months=months_to_predict-1)).strftime("%B_%Y")}.xlsx'
                with pd.ExcelWriter(combined_output_filename, engine='xlsxwriter') as writer:
                    for sheet_name, df in all_predictions.items():
                        df.to_excel(writer, sheet_name=sheet_name)
                
                st.success(f"Predictions generated for all requested months.")

                # Offer download button for the combined Excel file
                with open(combined_output_filename, "rb") as file:
                    btn = st.download_button(label="Download All Predictions", data=file, file_name=combined_output_filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
