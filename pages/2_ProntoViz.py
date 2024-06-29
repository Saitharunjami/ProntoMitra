import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time  # Add this import for timing animations

# Function to simulate document processing animation
def process_animation():
    st.info("Processing your document...")
    progress_bar = st.progress(0)
    for percent_complete in range(0, 101, 10):
        time.sleep(0.1)
        progress_bar.progress(percent_complete)
    st.success("Document processing complete!")

# Function to create line plots
def create_line_plot(data, x, ys, title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    for y in ys:
        plt.plot(data[x], data[y], marker='o', label=y)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.legend()
    return plt

# Function to create bar plots
def create_bar_plot(data, x, y, title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    plt.bar(data[x], data[y])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    return plt

# Streamlit app title
st.title('ProntoViz 📊')

# File upload section
st.sidebar.header('Upload File')
uploaded_file = st.sidebar.file_uploader("Upload an Excel file", type=["xlsx"])

# Add a link to view the format with an image
with st.sidebar.expander("View data format"):
    st.image('assets/formatprontoviz.png', use_column_width=True)  # Path to your image in the assets folder

# Display green box to upload file
if uploaded_file is None:
    st.sidebar.info("🟢 Upload a file to get started!")

# Function to load and process data
def load_data(file):
    if file is not None:
        try:
            # Show processing animation
            process_animation()

            # Load the provided Excel file
            data = pd.read_excel(file)

            # Convert timestamp columns to datetime with error coercion
            data['createdOn'] = pd.to_datetime(data['createdOn'], errors='coerce')
            data['regularizedOn'] = pd.to_datetime(data['regularizedOn'], errors='coerce')
            data['authorizedOn'] = pd.to_datetime(data['authorizedOn'], errors='coerce')

            # Drop rows with NaN values in 'createdOn'
            data = data.dropna(subset=['createdOn'])

            # Calculate time taken to regularize (in days)
            data['time_to_regularize'] = (data['regularizedOn'] - data['createdOn']).dt.total_seconds() / 86400

            # Calculate time taken to authorize (in days)
            data['time_to_authorize'] = (data['authorizedOn'] - data['regularizedOn']).dt.total_seconds() / 86400

            # Calculate overall time taken (in days)
            data['time_overall'] = (data['authorizedOn'] - data['createdOn']).dt.total_seconds() / 86400

            # Extract month and year from 'createdOn' column
            data['created_month'] = data['createdOn'].dt.month
            data['created_year'] = data['createdOn'].dt.year.astype(int)

            return data

        except Exception as e:
            st.error(f"Error: {e}")
            return None
    else:
        return None

# Display uploaded file data and analysis
if uploaded_file is not None:
    data = load_data(uploaded_file)

    if data is not None:
        # Mapping of month names to numbers
        months = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4,
            'May': 5, 'June': 6, 'July': 7, 'August': 8,
            'September': 9, 'October': 10, 'November': 11, 'December': 12
        }

        # Sidebar for month-wise summary
        st.sidebar.header('Filter Data')
        month_name = st.sidebar.selectbox('Select Month', list(months.keys()))
        year_input = st.sidebar.selectbox('Select Year', data['created_year'].unique())

        # Get the corresponding month number
        month_input = months[month_name]

        # Button to display month-wise summary
        if st.sidebar.button('Predict', key='predict'):
            # Show processing animation
            process_animation()

            # Filter data based on the selected month and year
            filtered_data = data[(data['created_month'] == month_input) & (data['created_year'] == year_input)]

            if not filtered_data.empty:
                # Summarize the data by employee
                summary_overall = filtered_data.groupby('allocatedTo').agg({
                    'time_to_regularize': 'mean',
                    'time_to_authorize': 'mean',
                    'time_overall': 'mean',
                    'createdOn': 'count'  # Use a different column name here if needed
                })

                # Reset index if necessary
                summary_overall.reset_index(inplace=True)

                # Rename columns and reorder
                summary_overall = summary_overall[['allocatedTo', 'createdOn', 'time_to_regularize', 'time_to_authorize', 'time_overall']]
                summary_overall.columns = ['Employee', 'Number of Documents', 'Avg Time to Regularize (days)', 'Avg Time to Authorize (days)', 'Avg Overall Time (days)']

                st.header(f"Overall Summary for {month_name} {year_input}")
                st.write(summary_overall)

                # Summarize the data by module and employee
                summary_module = filtered_data.groupby(['module', 'allocatedTo']).agg({
                    'time_to_regularize': 'mean',
                    'time_to_authorize': 'mean',
                    'time_overall': 'mean',
                    'createdOn': 'count'  # Use a different column name here if needed
                })

                # Reset index if necessary
                summary_module.reset_index(inplace=True)

                # Rename columns and reorder
                summary_module = summary_module[['module', 'allocatedTo', 'createdOn', 'time_to_regularize', 'time_to_authorize', 'time_overall']]
                summary_module.columns = ['Module', 'Employee', 'Number of Documents', 'Avg Time to Regularize (days)', 'Avg Time to Authorize (days)', 'Avg Overall Time (days)']

                st.header(f"Module-wise Summary for {month_name} {year_input}")

                # Display individual tables for each employee
                employees = summary_module['Employee'].unique()
                for employee in employees:
                    st.subheader(f"Employee: {employee}")
                    employee_data = summary_module[summary_module['Employee'] == employee]
                    st.write(employee_data)

                    # Create a line plot for Module-wise Summary for Entire Data by Employee
                    fig = create_line_plot(employee_data, 'Module', ['Avg Time to Regularize (days)', 'Avg Time to Authorize (days)', 'Avg Overall Time (days)'],
                                          f'Module-wise Metrics for {employee}', 'Module', 'Metrics')
                    st.pyplot(fig)

                    # Create a bar plot for Module-wise Summary for Entire Data by Employee
                    fig = create_bar_plot(employee_data, 'Module', 'Avg Overall Time (days)',
                                          f'Module-wise Avg Overall Time for {employee}', 'Module', 'Avg Overall Time (days)')
                    st.pyplot(fig)

            else:
                st.write("No data available for the selected month and year.")

    else:
        st.write("Please upload an Excel file.")

# Sidebar for overall summary
st.sidebar.header('Overall Data Analysis')
if st.sidebar.button('Calculate Overall Avg Time for Entire Data', key='overall_avg'):
    # Show processing animation
    process_animation()

    overall_avg = data[['time_to_regularize', 'time_to_authorize', 'time_overall']].mean()

    st.header("Overall Average Time for Entire Data")
    st.write(f"Avg Time to Regularize: {overall_avg['time_to_regularize']:.2f} days")
    st.write(f"Avg Time to Authorize: {overall_avg['time_to_authorize']:.2f} days")
    st.write(f"Avg Overall Time: {overall_avg['time_overall']:.2f} days")

    # Summarize the overall data by employee
    summary_overall_all = data.groupby('allocatedTo').agg({
        'time_to_regularize': 'mean',
        'time_to_authorize': 'mean',
        'time_overall': 'mean',
        'createdOn': 'count'  # Use a different column name here if needed
    })

    # Reset index if necessary
    summary_overall_all.reset_index(inplace=True)

    # Rename columns and reorder
    summary_overall_all = summary_overall_all[['allocatedTo', 'createdOn', 'time_to_regularize', 'time_to_authorize', 'time_overall']]
    summary_overall_all.columns = ['Employee', 'Number of Documents', 'Avg Time to Regularize (days)', 'Avg Time to Authorize (days)', 'Avg Overall Time (days)']

    st.header("Overall Summary for Entire Data")
    st.write(summary_overall_all)

    # Summarize the overall data by module and employee
    summary_module_all = data.groupby(['module', 'allocatedTo']).agg({
        'time_to_regularize': 'mean',
        'time_to_authorize': 'mean',
        'time_overall': 'mean',
        'createdOn': 'count'  # Use a different column name here if needed
    })

    # Reset index if necessary
    summary_module_all.reset_index(inplace=True)

    # Rename columns and reorder
    summary_module_all = summary_module_all[['module', 'allocatedTo', 'createdOn', 'time_to_regularize', 'time_to_authorize', 'time_overall']]
    summary_module_all.columns = ['Module', 'Employee', 'Number of Documents', 'Avg Time to Regularize (days)', 'Avg Time to Authorize (days)', 'Avg Overall Time (days)']

    st.header("Module-wise Summary for Entire Data")

    # Display individual tables for each employee
    employees_all = summary_module_all['Employee'].unique()
    for employee in employees_all:
        st.subheader(f"Employee: {employee}")
        employee_data_all = summary_module_all[summary_module_all['Employee'] == employee]
        st.write(employee_data_all)

        # Create a line plot for Module-wise Summary for Entire Data by Employee
        fig = create_line_plot(employee_data_all, 'Module', ['Avg Time to Regularize (days)', 'Avg Time to Authorize (days)', 'Avg Overall Time (days)'],
                              f'Module-wise Metrics for {employee}', 'Module', 'Metrics')
        st.pyplot(fig)

        # Create a bar plot for Module-wise Summary for Entire Data by Employee
        fig = create_bar_plot(employee_data_all, 'Module', 'Avg Overall Time (days)',
                              f'Module-wise Avg Overall Time for {employee}', 'Module', 'Avg Overall Time (days)')
        st.pyplot(fig)