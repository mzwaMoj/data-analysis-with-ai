# agent_generate_plot_code/generate_plots.py
from pathlib import Path
import sys
import os

# Add the src directory to the Python path
src_dir = str(Path(__file__).parent.parent)
sys.path.append(src_dir)

import pandas as pd
import openai, json
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import Image, display
import io
import os
import ast
import tempfile
import warnings
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
warnings.filterwarnings("ignore")
load_dotenv(find_dotenv())

from agent_generate_plot_code.prompts import prompt_agent_generate_plot_code

# Set OpenAI API key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Function that generates Python code for plotting based on user query and dataframe
def generate_plot_code(user_request, df):
    """Generate Python code for plotting."""
    prompt = prompt_agent_generate_plot_code(df)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt},
                  {"role": "user", "content": f"\n###user_request: {user_request}"}],
        temperature=0.3,
    )
    generated_code = response.choices[0].message.content
    return generated_code

# # Function to execute the generated Python code and display the plot
# def execute_plot_code(code, df):
#     """Execute the generated Python code and display the plot."""
#     try:
#         # Parse the input code
#         code = code.strip("```python\n").strip("```")
#         parsed_code = ast.parse(code)

#         # Define the function to execute the code
#         def plot_function(df):
#             exec_globals = {"df": df, "plt": plt, "pd": pd}
#             exec(compile(parsed_code, filename="<ast>", mode="exec"), exec_globals)

#         # Execute the function
#         plot_function(df)

#         # Save the plot to a temporary file
#         temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
#         plt.savefig(temp_file.name, format="png")
#         plt.close()

#         # Display the image
#         display(Image(filename=temp_file.name))
#         # return temp_file.name;
#     except Exception as e:
#         return f"Error executing code: {str(e)}"
    
def execute_plot_code(code, df):
    """Execute the generated Python code and return the plot as an image."""
    try:
        # Parse the input code
        code = code.strip("```python\n").strip("```")
        parsed_code = ast.parse(code)
        
        # Create a new figure
        plt.figure(figsize=(10, 6))
        
        # Execute the code with the dataframe
        exec_globals = {"df": df, "plt": plt, "pd": pd}
        exec(compile(parsed_code, filename="<ast>", mode="exec"), exec_globals)
        
        # Save the plot to a bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', dpi=300)
        plt.close()
        
        # Convert to PIL Image
        buf.seek(0)
        return Image.open(buf)
    except Exception as e:
        return f"Error executing code: {str(e)}"