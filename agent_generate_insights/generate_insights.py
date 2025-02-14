from pathlib import Path
import sys
import os

# Add the src directory to the Python path
src_dir = str(Path(__file__).parent.parent)
sys.path.append(src_dir)

import pandas as pd
import numpy as np
import openai, json
import os, ast, tempfile, warnings
from dotenv import load_dotenv, find_dotenv
from datetime import datetime
from openai import OpenAI
warnings.filterwarnings("ignore")
load_dotenv(find_dotenv())

from agent_generate_insights.prompts import prompt_insights_agent, prompt_compute_agent

# Set OpenAI API key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


# 1. Function that generates Python code for plotting based on user query and dataframe
def agent_generate_compute_code(query, df):
    """Generate Python code for plotting."""
    prompt = prompt_compute_agent()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt + f"\n###Use these dataframe features: {df.columns}"},
                  {"role": "user", "content": query}],
        temperature=0.3,
    )
    generated_code = response.choices[0].message.content
    print("Generated compute code: \n", generated_code)
    return generated_code

# 2. Function that executes the generated function code and returns the computed values
def execute_function_code(function_code, df):
    """
    Executes the generated function code and returns the computed values.
    Args:
        function_code (str): The function code as a string, wrapped in ```code``` blocks.
        df (pd.DataFrame): The DataFrame to pass as input to the function.
    Returns:
        dict: The computed values from the function.
    """
    try:
        # Parse the input code
        function_code = function_code.strip("```python\n").strip("```")
        parsed_code = ast.parse(function_code)

        # Extract the function name from the code
        function_name = None
        for node in ast.walk(parsed_code):
            if isinstance(node, ast.FunctionDef):
                function_name = node.name
                break

        if not function_name:
            return "Error: No function definition found in the code."

        # Define the function to execute the code
        def compute_values(df):
            exec_globals = {"df": df, "pd": pd}
            exec_locals = {}
            exec(compile(parsed_code, filename="<ast>", mode="exec"), exec_globals, exec_locals)
            return exec_locals.get(function_name)(df)

        # Execute the function and return the results
        print("Executing function code...\n",compute_values(df))
        return compute_values(df)
    except Exception as e:
        return f"Error executing code: {str(e)}"

# 3. Function that generates insights based on user query and dataframe
def agent_generate_insights_agent(query, user_request):
    """Generate Python code for plotting."""
    prompt = prompt_insights_agent()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt + f"\n###user_request: {user_request}"},
                  {"role": "user", "content": f"{query}"}],
        temperature=0.3,
    )
    output = response.choices[0].message.content
    return output

# 4. Function that chains the above functions to generate insights
def agent_generate_insights(function_code, df, user_request):
    """
    Generate insights by chaining the following steps:
    1. Generate compute code from plot code using `agent_generate_compute_code`.
    2. Execute the compute code using `execute_function_code`.
    3. Generate insights based on the computed values and user query.

    Args:
        function_code (str): The original plot code as a string.
        df (pd.DataFrame): The DataFrame to analyze.
        query (str): The user's query for generating insights.

    Returns:
        str: Generated insights as a string.
    """
    # Step 1: Generate compute code
    compute_code = agent_generate_compute_code(function_code, df)
    # Step 2: Execute the compute code
    computed_values = execute_function_code(compute_code, df)
    # Step 3: Generate insights
    insights = agent_generate_insights_agent(computed_values, user_request)
    return insights