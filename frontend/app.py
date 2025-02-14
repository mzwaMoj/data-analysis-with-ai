import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import io, tempfile, ast
from agent_router.routing_agent import routing_agent
from agent_generate_plot_code.generate_plots import execute_plot_code as original_execute_plot_code
from pathlib import Path
import sys

# Add the src directory to the Python path
src_dir = str(Path(__file__).parent.parent)
sys.path.append(src_dir)

def execute_plot_code(code, df):
    """Execute the generated Python code and return the plot as an image or an error message."""
    try:
        # Clean the code string
        code = code.strip("```python\n").strip("```")
        parsed_code = ast.parse(code)
        
        # Create a new figure
        plt.figure(figsize=(10, 6))
        
        # Execute the code with the dataframe
        exec_globals = {"df": df, "plt": plt, "pd": pd}
        exec(compile(parsed_code, filename="<ast>", mode="exec"), exec_globals)
        
        # Save the plot to a buffer
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
        if file.name.endswith(".csv"):
            df = pd.read_csv(file.name)
        elif file.name.endswith(".xlsx"):
            df = pd.read_excel(file.name)
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
            elif result["type"] in ["insights", "error"]:
                text_output = result["content"]
        except Exception as e:
            text_output = f"Error processing request: {str(e)}"
    else:
        text_output = "No analysis request provided yet."
    
    return plot_output, text_output, summary, head

# Custom CSS for better styling
custom_css = """
.container {
    max-width: 1200px !important;
    margin: auto !important;
}
.output-image {
    border: 1px solid #ddd !important;
    border-radius: 8px !important;
    padding: 10px !important;
}
.output-text {
    border: 1px solid #ddd !important;
    border-radius: 8px !important;
    padding: 15px !important;
    margin-top: 10px !important;
    background-color: #f8f9fa !important;
}
.dataframe {
    font-size: 12px !important;
    margin-top: 10px !important;
}
"""

with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("# Interactive Data Visualization and Analysis")
    gr.Markdown("Upload your dataset and describe what you’d like to visualize or analyze.")
    
    with gr.Row():
        # Left column for data summary
        with gr.Column(scale=1):
            file_input = gr.File(label="Upload Dataset (CSV/Excel)")
            summary_table = gr.DataFrame(label="Data Summary", interactive=False)
            head_table = gr.DataFrame(label="First Five Rows", interactive=False)
        
        # Right column for visualization and analysis
        with gr.Column(scale=2):
            output_box = gr.Image(label="Visualization Output", height=400, container=True)
            # Changed Analysis Output from Textbox to Markdown to allow markdown formatting
            text_output = gr.Markdown(
                value="Detailed analysis output will appear here...",
                label="Analysis Output"
            )
            user_query = gr.Textbox(
                label="What would you like to visualize or analyze?",
                placeholder="e.g., 'Create a line plot of sales over time' or 'Analyze the sales trends'",
                lines=2
            )
            generate_btn = gr.Button("Generate", variant="primary")
    
    # Set up event handlers
    file_input.change(
        fn=process_request,
        inputs=[file_input, user_query],
        outputs=[output_box, text_output, summary_table, head_table]
    )
    
    generate_btn.click(
        fn=process_request,
        inputs=[file_input, user_query],
        outputs=[output_box, text_output, summary_table, head_table]
    )

demo.launch()
