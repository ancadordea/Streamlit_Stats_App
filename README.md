# Statpy: Simple Statistical Testing 

**Statpy** is a lightweight, browser-based web app built with **Streamlit** that helps users perform common statistical tests—**no coding required**.

Whether you're a researcher, clinician, student, or analyst, Statpy provides a guided, no-code environment for:

- Uploading your dataset
- Selecting variables
- Automatically choosing the right statistical test
- Checking assumptions
- Running the analysis
- Visualising your data and simple interpretations

---

## Why Use Statpy?

Many people who work with data don’t code. Statpy makes statistical testing accessible by removing technical barriers.

-  **Fast**: Upload data, run tests, get visual results in minutes
-  **Smart**: Automatically suggests the correct test (e.g., t-test, ANOVA, Chi-square, correlation)
-  **Statistical**: Includes assumption checks (e.g., normality, group size)
-  **Visual**: Built-in charts and plots
-  **Interpretation**: Plain-language summaries of results
-  **For Everyone**: Designed for people without coding backgrounds

---

##  Who It's For

- Researchers 
- Students learning statistics
- Educators needing a classroom-friendly statistical demo
- Analysts running quick hypothesis checks
- Teams wanting reusable, browser-based workflows

---

##  What It Does

###  1. Data Upload
- Supports `.csv` and `.xlsx` files
- Shows preview of uploaded data

###  2. Variable Selection
- Select two variables: X (numeric or continuous) and Y (grouping or categorical)
- Statpy infers data types and test requirements

###  3. Test Suggestions & Assumptions
- Automatically suggests the right test:
  - T-test
  - ANOVA
  - Chi-square
  - Correlation (Pearson/Spearman)
- Checks for:
  - Missing data
  - Normal distribution (Shapiro test)
  - Group sizes

###  4. Results
- Outputs test statistics (e.g., p-value, t-statistic, correlation)
- Gives simple interpretation (e.g., “statistically significant”)
- Generates charts:
  - Box plots
  - Scatter plots
  - Bar charts

---

## R/Python vs. Statpy – Why Use This Instead?

- There is no programming required
- Easy for Non-Tech Users
- Interactive Controls
- Instant Visualization
- Simple UI and Workflow

It is perfect for brainstorming ideas for your data!

---

##  Installation

### Requirements
- Python 3.7 or higher

### Setup
```bash
pip install -r requirements.txt
```

### Run the App
```bash
streamlit run app.py
```
---

## How It Works Under the Hood

- Summary statistics and tests powered by:
  - `scipy.stats` for t-tests, ANOVA, chi-square, Shapiro, correlation
  - `pandas` for data handling
  - `matplotlib` and `seaborn` for plotting
- Missing values are automatically excluded before analysis
- Correlation method (Pearson vs. Spearman) is chosen based on data normality

---

##  Future Features

- Paired tests (e.g., paired t-test)
- Non-parametric tests (e.g., Mann-Whitney U, Kruskal-Wallis)
- Multiple regression
- Exportable PDF reports
- Session memory for reproducibility
