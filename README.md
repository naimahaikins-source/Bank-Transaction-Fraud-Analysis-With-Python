# Bank-Transaction-Fraud-Analysis-With-Python
Bank transaction fraud analysis using Python, Pandas, and Streamlit to identify fraud patterns, analyze transaction amounts, and visualize findings in an interactive dashboard.
# Bank Transaction Fraud Analysis with Python

An exploratory data analysis project focused on identifying transaction fraud patterns, examining fraudulent transaction amounts, and communicating insights through data visualization and an interactive Streamlit dashboard.

## Project Overview

Financial fraud presents significant challenges for banks and financial institutions, resulting in financial losses and reduced customer trust. This project uses Python-based data analysis to explore bank transaction fraud, identify patterns across fraud categories, and generate insights that can support better fraud monitoring and decision-making.

The project combines data cleaning, exploratory data analysis (EDA), statistical summaries, data visualization, and interactive dashboard development.

## Objectives

- Explore the structure and quality of the transaction dataset.
- Analyze fraud cases across different fraud types.
- Examine transaction amounts associated with reported fraud.
- Compare fraud categories using descriptive statistics.
- Visualize key findings to make patterns easier to understand.
- Develop an interactive dashboard for exploring the results.

## Tools and Technologies

- **Python** — data analysis and scripting
- **Pandas** — data manipulation and analysis
- **NumPy** — numerical operations
- **Matplotlib and Seaborn** — data visualization, where applicable
- **Jupyter Notebook / Google Colab** — analysis environment
- **Streamlit** — interactive dashboard development

## Project Workflow

1. **Data loading:** Imported the transaction dataset into Python.
2. **Data inspection:** Examined the dataset's structure, columns, data types, and missing values.
3. **Data preparation:** Reviewed data quality and prepared relevant fields for analysis.
4. **Exploratory data analysis:** Investigated fraud categories and transaction amounts.
5. **Statistical analysis:** Calculated relevant summary measures, including case counts, total amounts, averages, and medians where applicable.
6. **Data visualization:** Created charts to communicate important patterns.
7. **Dashboard development:** Built an interactive Streamlit application to present the analysis.

## Visualizations and Key Insights

The following visualizations highlight different aspects of the analysis. Replace the image filenames below with the exact names of the chart screenshots uploaded to the `images` folder.

### 1. Fraud Distribution

![Fraud Distribution](images/fraud_distribution.png)

*Purpose: To illustrate the distribution of fraud cases across the categories included in the dataset.*

### 2. Fraud by Type

![Fraud by Type](images/fraud_type_analysis.png)

*Purpose: To compare fraud categories by the number of reported cases and identify categories that warrant further investigation.*

### 3. Fraudulent Transaction Amounts

![Fraud Amount Analysis](images/fraud_amount_analysis.png)

*Purpose: To examine transaction amounts associated with fraud and compare the financial impact across relevant categories.*

### Key Findings

The analysis examines differences in fraud frequency and transaction amounts across fraud categories. The final findings should be interpreted using the calculated results and visualizations from the notebook.

Specific figures and conclusions will be added here after the final results have been verified.

## Interactive Dashboard

The project includes a Streamlit dashboard designed to make the analysis easier to explore.

**Dashboard:** [Add your deployed Streamlit URL here]

The dashboard is intended to help users explore fraud-related patterns and review the key findings interactively.

## Repository Structure

```text
Bank-Transaction-Fraud-Analysis-With-Python/
│
├── Bank_Transaction_Fraud_Analysis_.ipynb
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── images/
    ├── fraud_distribution.png
    ├── fraud_type_analysis.png
    └── fraud_amount_analysis.png
```

*The `images/` folder and its contents should be added to the repository as the chart screenshots are uploaded.*

## How to Run the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/naimahaikins-source/Bank-Transaction-Fraud-Analysis-With-Python.git
```

### 2. Navigate to the project directory

```bash
cd Bank-Transaction-Fraud-Analysis-With-Python
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit dashboard

```bash
streamlit run app.py
```

Ensure that the dataset is available at the location expected by `app.py`.

## Limitations

- The findings depend on the quality, completeness, and scope of the available dataset.
- Observed patterns do not necessarily establish the causes of fraudulent transactions.
- The analysis should not be treated as a production-ready fraud detection system without further validation and testing.

## Future Improvements

- Add additional fraud indicators and transaction-level comparisons.
- Develop more detailed time-based fraud analysis if suitable date fields are available.
- Explore machine learning techniques for fraud classification.
- Improve dashboard filtering and reporting capabilities.
- Evaluate potential fraud detection models using appropriate performance metrics.

## Author

**Naimat Aikins-Mustapha**

Data Analyst | Economics Student

GitHub: [@naimahaikins-source](https://github.com/naimahaikins-source)

---

*This project demonstrates the application of Python, exploratory data analysis, statistical summaries, and data visualization to a financial fraud analysis problem.*
