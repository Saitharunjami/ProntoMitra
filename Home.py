import streamlit as st

st.set_page_config(
    page_title="Pronto Mitra",
    page_icon="assets/lnt_logo.png",
)

# Correctly capitalized "Pronto Mitra" in sidebar
st.sidebar.markdown("<h1 style='font-size: 24px;'>Pronto Mitra</h1>", unsafe_allow_html=True)


st.sidebar.image('assets/logo_1_1.png', width=250)

st.write("# Welcome to Pronto Mitra 👋")

st.sidebar.success("Select a Tool above.")

st.markdown(
    """
    Pronto Mitra serves as the central dashboard in our project, integrating two key models to enhance our document management and predictive capabilities. The dashboard is designed to provide comprehensive insights and predictions to streamline our processes and improve efficiency.
"""
)

with st.expander("About Pronto Genie"):
    st.write("")
    st.write("""Pronto Genie is the prediction model within Pronto Mitra, focused on forecasting document counts based on various input parameters. By leveraging machine learning techniques, Pronto Genie enables us to anticipate the number of documents that will be received in future periods, thus facilitating better planning and resource allocation.""")
    st.write("•	Key Features:")
    st.write("o	Data Input: Users can upload data files containing historical document records.")
    st.write("o	Data Processing: The model preprocesses the data, extracting relevant features such as date, job code, and module.")
    st.write("o	Model Training: Pronto Genie utilizes Ridge regression with polynomial features, selected for its ability to capture non-linear relationships and prevent overfitting.")
    st.write("o	Prediction: The model predicts future document counts for specified months, providing day-wise and module-wise breakdowns.")
    st.write("o Visualization: The predictions are visualized through graphs and tables, offering a clear view of the expected document inflow.")
    


with st.expander("About Pronto Viz"):
    st.write("")
    st.write("""Pronto Viz is the data analysis Tool within Pronto Mitra, designed to analyze the time taken by employees to process documents. This tool plays a crucial role in document allocation and resource management, ensuring that tasks are distributed efficiently and employee performance is monitored effectively.""")
    st.write("•	Key Features:")
    st.write("o	Data Input: Users can upload data files detailing employee processing times and document handling.")
    st.write("o	Data Analysis: The tool analyzes the time taken for each document, identifying patterns and bottlenecks in the process.")
    st.write("o	Resource Management: Based on the analysis, Pronto Viz provides insights into optimal document allocation, ensuring that workload is balanced among employees.")
    st.write("o	Performance Monitoring: The tool helps track employee performance over time, identifying areas for improvement and training needs.")
    st.write("o •	Visualization: Results are presented through intuitive charts and dashboards, highlighting key metrics and performance indicators.")
    
#st.button("Manual for Pronto Genie")

#st.button("Manual for Pronto Viz")

# col1, col2 = st.columns([1, 2])  # Adjust the width ratio as needed

#     # Place the image in the first column
# with col1:
#     st.button("Manual for Pronto Genie")
        
        

#     # Place the title in the second column
# with col2:
#         st.button("Manual for Pronto Viz")



# Embedding PDF files in the main page
col1, col2 = st.columns([1, 2])  # Adjust the width ratio as needed

with col1:
    if st.button("Manual for Pronto Genie"):
        st.markdown("<iframe src='assets/Pronto Genie User Manual.pdf' width='100%' height='600px'></iframe>", unsafe_allow_html=True)

with col2:
    if st.button("Manual for Pronto Viz"):
        st.markdown("<iframe src='assets/ProntoViz User Manual.pdf' width='100%' height='600px'></iframe>", unsafe_allow_html=True)

        


# Your Streamlit app content here

# Add the footer with modern styling
st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(0, 0, 0, 0.5); /* Transparent background */
        color: white; /* White text color */
        text-align: center;
        padding: 2px;
        font-size: 14px;
        border-top: 0.5px solid #eaeaea;
    }
    </style>
    <div class="footer">
        <p>Developed by Jami Sai Tharun and Habeeb Ur Rahman</p>
    </div>
    """, unsafe_allow_html=True)
