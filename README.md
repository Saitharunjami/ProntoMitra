

# Pronto Mitra: The Main Dashboard
<img src="https://github.com/Saitharunjami/ProntoMitra/blob/main/assets/logo_1_1.png" alt="Pronto Mitra" width="200" />

Welcome to **Pronto Mitra**, the comprehensive dashboard designed to enhance document management and predictive capabilities through advanced machine learning techniques. This project integrates two powerful models: **Pronto Genie** and **Pronto Viz**, providing insightful predictions and data analysis to streamline processes and improve efficiency.

## Table of Contents

- [Introduction](#introduction)
- [Pronto Genie (Prediction Model)](#pronto-genie-prediction-model)
- [Pronto Viz (Data Analysis Tool)](#pronto-viz-data-analysis-tool)
- [Integration and Benefits](#integration-and-benefits)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Acknowledgements](#acknowledgements)
- [License](#license)

## Introduction

Pronto Mitra serves as the central dashboard in our project, integrating two key models to enhance our document management and predictive capabilities. The dashboard provides comprehensive insights and predictions to streamline processes and improve efficiency.

## Pronto Genie (Prediction Model)

Pronto Genie is the prediction model within Pronto Mitra, focused on forecasting document counts based on various input parameters. By leveraging machine learning techniques, Pronto Genie enables anticipation of document inflow, facilitating better planning and resource allocation.

### Key Features:
- **Data Input**: Upload historical document records.
- **Data Processing**: Preprocess data, extracting relevant features like date, job code, and module.
- **Model Training**: Utilize Ridge regression with polynomial features for capturing non-linear relationships and preventing overfitting.
- **Prediction**: Predict future document counts with day-wise and module-wise breakdowns.
- **Visualization**: Visualize predictions through graphs and tables.

## Pronto Viz (Data Analysis Tool)

Pronto Viz is the data analysis tool within Pronto Mitra, designed to analyze the time taken by employees to process documents. This tool plays a crucial role in document allocation and resource management.

### Key Features:
- **Data Input**: Upload data detailing employee processing times and document handling.
- **Data Analysis**: Analyze processing times, identifying patterns and bottlenecks.
- **Resource Management**: Provide insights into optimal document allocation.
- **Performance Monitoring**: Track employee performance over time.
- **Visualization**: Present results through intuitive charts and dashboards.

## Integration and Benefits

By integrating Pronto Genie and Pronto Viz within the Pronto Mitra dashboard, we achieve a holistic view of the document management process. The predictive capabilities of Pronto Genie, combined with the analytical insights of Pronto Viz, empower us to:
- **Optimize Resource Allocation**: Ensure documents are assigned to the right employees at the right time.
- **Improve Efficiency**: Anticipate document inflow and prepare accordingly.
- **Enhance Performance Monitoring**: Continuously track and improve employee performance.
- **Streamline Operations**: Achieve a smoother and more efficient document management process.

Pronto Mitra stands as a powerful tool, driving data-driven decisions and fostering a more efficient work environment.

[**Access Pronto Mitra**](https://prontomitra.streamlit.app/)

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

Ensure you have the following installed:
- Python 3.x
- Streamlit
- Pandas
- Matplotlib

### Installation

1. Clone the repo:
    ```sh
    git clone https://github.com/your-username/pronto-mitra.git
    ```
2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

### Running the App

```sh
streamlit run Home.py
```

## Usage

1. **Pronto Genie**: Upload historical document data to get predictions on future document inflow.
2. **Pronto Viz**: Upload employee processing data to analyze processing times and optimize resource allocation.

## Screenshots

<img src="https://github.com/Saitharunjami/ProntoMitra/blob/main/assets/Main%20Dashboard.png" alt="Pronto Mitra" width="250" />

<img src="https://github.com/Saitharunjami/ProntoMitra/blob/main/assets/Prontogeniedashboard.png" alt="Pronto Genie" width="250" />

<img src="https://github.com/Saitharunjami/ProntoMitra/blob/main/assets/ProntoVizdashboard.png" alt="Pronto Viz" width="250" />


## Acknowledgements

We are deeply thankful to **Mr. G. Kartik**, Head of the Corporate Centre, PT&D IC, L&T Construction, for his exceptional guidance and support throughout the duration of our project. His insights and expertise have been instrumental in the successful completion of our work. His encouragement and constructive feedback have greatly enhanced our learning experience.

Our sincere thanks also go to **Mr. Sahil Kumar Singh**, who guided us for the entire project, provided invaluable guidance throughout the entire project, offering crucial assistance whenever we encountered challenges. **Mr. Sudeesh B**, and **Mr. Mahanaraj Paul**, who help use with the data, instrumental in managing the data, handling Excel operations and verifying results, ensuring the integrity and accuracy of our work. Sincere thanks to staff at L&T Construction who have supported and guided us during this internship. Their willingness to share their knowledge and assist us in various aspects of the project has been crucial to our success.

## License
Copyright (c) 2024 **Jami Sai Tharun** and **Habeeb Ur Rahman**



