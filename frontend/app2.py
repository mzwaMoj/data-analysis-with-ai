from pathlib import Path
import sys
# Add the src directory to the Python path
src_dir = str(Path(__file__).parent.parent)
sys.path.append(src_dir)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import io, ast
from agent_router.routing_agent import routing_agent
from agent_generate_plot_code.generate_plots import execute_plot_code as original_execute_plot_code
import warnings
warnings.filterwarnings("ignore")

# Set page configuration
st.set_page_config(
    page_title="Data Visualization and Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Components
st.sidebar.title("📂 Upload & Data Preview")

# File uploader
uploaded_file = st.sidebar.file_uploader(
    "Upload Dataset (CSV/Excel)",
    type=["csv", "xlsx"],
    help="Upload a CSV or Excel file to begin."
)

def execute_plot_code(code, df):
    """Execute the generated Python code and return the plot as an image or an error message."""
    try:
        code = code.strip("```python\n").strip("```")
        parsed_code = ast.parse(code)
        
        plt.figure(figsize=(10, 6))
        exec_globals = {"df": df, "plt": plt, "pd": pd}
        exec(compile(parsed_code, filename="<ast>", mode="exec"), exec_globals)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=300)
        plt.close()
        
        buf.seek(0)
        return Image.open(buf), ""
    except Exception as e:
        return None, f"**Error executing plot code:** {str(e)}"

def load_data(file):
    """Load dataset from CSV or Excel."""
    try:
        # Reset read pointer to the beginning of the file
        file.seek(0)
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(file)
        else:
            raise ValueError("Unsupported file format")
        return df
    except Exception as e:
        return str(e)

def process_request(file, user_request):
    """Handle file upload and visualization request."""
    plot_output = None
    text_output = ""
    summary = pd.DataFrame()
    head = pd.DataFrame()
    
    if file is None:
        text_output = "Please upload a dataset file."
        return plot_output, text_output, summary, head
    
    df = load_data(file)
    if isinstance(df, str):  # Error message from load_data
        text_output = f"Error loading data: {df}"
        return plot_output, text_output, summary, head
    
    summary, head = df.describe().reset_index(), df.head()
    
    if user_request:
        try:
            result = routing_agent(user_request, df)
            if result["type"] == "plot":
                plot_output, plot_error = execute_plot_code(result["content"], df)
                if plot_error:
                    text_output = plot_error
            elif result["type"] == "insights":
                text_output = result["content"]
            elif result["type"] == "plot_and_insights":
                plot_output, plot_error = execute_plot_code(result["content"]["plot"], df)
                text_output = result["content"]["insights"]
                if plot_error:
                    text_output = plot_error
            elif result["type"] == "error":
                text_output = result["content"]
        except Exception as e:
            text_output = f"Error processing request: {str(e)}"
    else:
        text_output = "No analysis request provided yet."
    
    return plot_output, text_output, summary, head

# Load and display data summary in sidebar
if uploaded_file:
    df = load_data(uploaded_file)
    if isinstance(df, pd.DataFrame):
        st.sidebar.markdown("### Data Summary")
        st.sidebar.dataframe(df.describe())
        st.sidebar.markdown("### Data Snippet")
        st.sidebar.dataframe(df.head())
    else:
        st.sidebar.error(f"Error loading data: {df}")

# Main Section
st.title("📊 Data Visualization and Analysis")
st.markdown("Describe what you’d like to visualize or analyze.")

# User input for analysis
user_request = st.text_area(
    "What would you like to visualize or analyze?",
    placeholder="e.g., 'Create a line plot of sales over time and provide insights'",
    height=100
)

# Generate button
if st.button("Generate", key="generate_btn"):
    if uploaded_file is None:
        st.warning("Please upload a dataset file.")
    else:
        plot_output, text_output, summary, head = process_request(uploaded_file, user_request)
        
        # Display results
        if plot_output:
            st.markdown("### Visualization Output")
            st.image(plot_output, caption="Generated Plot", use_container_width =True)
        
        if text_output:
            st.markdown("### Analysis Output")
            st.markdown(text_output)