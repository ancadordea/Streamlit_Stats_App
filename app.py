import streamlit as st
import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Statpy - Statistics for everyone", layout="wide")
st.set_page_config(
    page_title="Statpy - Statistics for everyone",
    layout="wide",
    page_icon="📊"  
)

# Initialisation
if "step" not in st.session_state:
    st.session_state.step = 1
if "df" not in st.session_state:
    st.session_state.df = None

# Navigation Buttons
def next_step(): st.session_state.step += 1
def prev_step(): st.session_state.step -= 1

# Helpers
def infer_variable_type(series):
    if pd.api.types.is_numeric_dtype(series):
        if series.nunique() <= 10:
            return 'Categorical (numeric)'
        else:
            return 'Continuous'
    else:
        return 'Categorical'

def suggest_test(x_type, y_type, y_levels=None):
    if x_type == 'Continuous' and y_type == 'Categorical':
        return 'T-test' if y_levels == 2 else 'ANOVA'
    elif x_type == 'Categorical' and y_type == 'Categorical':
        return 'Chi-square test'
    elif x_type == 'Continuous' and y_type == 'Continuous':
        return 'Correlation (Pearson/Spearman)'
    return 'Unknown'

def check_assumptions(df, x, y, test):
    warnings = []
    if df[x].isnull().any() or df[y].isnull().any():
        warnings.append("! Missing values detected.")
    if test in ['T-test', 'ANOVA']:
        if df[y].value_counts().min() < 5:
            warnings.append("! Small group sizes.")
        if stats.shapiro(df[x])[1] < 0.05:
            warnings.append("! X may not be normally distributed.")
    return warnings

def run_test(df, x, y, test):
    result = {}
    if test == 'T-test':
        groups = df[y].dropna().unique()
        data1 = df[df[y] == groups[0]][x].dropna()
        data2 = df[df[y] == groups[1]][x].dropna()
        t_stat, p_val = stats.ttest_ind(data1, data2)
        result = {"t-statistic": t_stat, "p-value": p_val}
    elif test == 'ANOVA':
        groups = [group[x].dropna() for name, group in df.groupby(y)]
        f_stat, p_val = stats.f_oneway(*groups)
        result = {"F-statistic": f_stat, "p-value": p_val}
    elif test == 'Chi-square test':
        contingency = pd.crosstab(df[x], df[y])
        chi2, p_val, _, _ = stats.chi2_contingency(contingency)
        result = {"Chi²": chi2, "p-value": p_val}
    elif test.startswith("Correlation"):
        x_data = df[x].dropna()
        y_data = df[y].dropna()
        if stats.shapiro(x_data)[1] > 0.05 and stats.shapiro(y_data)[1] > 0.05:
            corr, p_val = stats.pearsonr(x_data, y_data)
            method = "Pearson"
        else:
            corr, p_val = stats.spearmanr(x_data, y_data)
            method = "Spearman"
        result = {"Correlation": corr, "p-value": p_val, "method": method}
    return result

def interpret_result(test, result):
    p = result.get("p-value", 1)
    if p < 0.05:
        sig = "statistically significant"
    else:
        sig = "not statistically significant"
    return f"The {test} yielded a p-value of {p:.4f}, which is {sig}."

# Upload Data
if st.session_state.step == 1:
    st.title("Step 1: Upload Your Dataset")
    file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
    if file:
        df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
        st.session_state.df = df
        st.dataframe(df.head())
        st.success(" File loaded successfully.")
        st.button("Next ->", on_click=next_step)

# === Step 2: Variable Selection ===
elif st.session_state.step == 2:
    st.title("Step 2: Select Variables for Analysis")
    df = st.session_state.df
    cols = df.columns.tolist()

    x = st.selectbox("Choose a continuous/numerical variable (X)", cols)
    y = st.selectbox("Choose a grouping variable (Y)", [c for c in cols if c != x])

    x_type = infer_variable_type(df[x])
    y_type = infer_variable_type(df[y])
    y_levels = df[y].nunique()
    test = suggest_test(x_type, y_type, y_levels)

    st.markdown(f"** Suggested Test:** {test}")
    with st.expander(" Why this test?"):
        st.write(f"X is {x_type}, Y is {y_type}, levels: {y_levels} → Suggest: **{test}**")

    st.session_state.x = x
    st.session_state.y = y
    st.session_state.test = test

    col1, col2 = st.columns(2)
    col1.button("<- Back", on_click=prev_step)
    col2.button(" Next ->", on_click=next_step)

# Assumptions and Test 
elif st.session_state.step == 3:
    st.title("Step 3: Assumption Checks & Run Test")

    df = st.session_state.df
    x, y = st.session_state.x, st.session_state.y
    test = st.session_state.test

    warnings = check_assumptions(df, x, y, test)
    if warnings:
        for w in warnings:
            st.warning(w)
    else:
        st.success("All assumption checks passed ")

    if st.button("▶ Run Analysis"):
        results = run_test(df, x, y, test)
        interpretation = interpret_result(test, results)

        st.session_state.results = results
        st.session_state.interpretation = interpretation
        next_step()

    st.button("<- Back", on_click=prev_step)

# Results & Export 
elif st.session_state.step == 4:
    st.title("Step 4: Results & Export")
    results = st.session_state.results
    interpretation = st.session_state.interpretation
    x, y, test = st.session_state.x, st.session_state.y, st.session_state.test
    df = st.session_state.df

    st.subheader(" Test Results")
    st.json(results)

    st.subheader(" Interpretation")
    st.markdown(f"**{interpretation}**")

    st.subheader(" Visualization")
    fig, ax = plt.subplots()
    if test in ["T-test", "ANOVA"]:
        sns.boxplot(x=df[y], y=df[x], ax=ax)
    elif test.startswith("Correlation"):
        sns.scatterplot(x=df[x], y=df[y], ax=ax)
    elif test == "Chi-square test":
        pd.crosstab(df[x], df[y]).plot(kind="bar", stacked=True, ax=ax)
    st.pyplot(fig)

    st.button("<- Back", on_click=prev_step)
