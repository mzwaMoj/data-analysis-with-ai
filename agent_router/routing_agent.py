# agent_router/routing_agent.py
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
import io, os, ast, tempfile, warnings
from agent_calls.functions import function_descriptions
from agent_generate_plot_code.generate_plots import generate_plot_code
from agent_generate_insights.generate_insights import agent_generate_insights
from agent_router.prompt_agent_router import prompt_agent_router
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
warnings.filterwarnings("ignore")
load_dotenv(find_dotenv())

# Set OpenAI API key
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# define a routing agent function
def routing_agent(user_request, df):
    """Routes the user request to the appropriate function/tool."""

    prompt = prompt_agent_router()
    messages = [
        {"role": "system", "content": f"{prompt}"},
        {"role": "user", "content": f"### User Request:\n{user_request}"}
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=messages,
        functions=function_descriptions(),
        function_call="auto"
    )
    message = response.choices[0].message
    function_calls = message.function_call 
    # print("Function called: ", function_calls)
    if function_calls:
        function_name = function_calls.name
        function_args = function_calls.arguments
        if function_name == "generate_plot_code":
            arguments = json.loads(function_args)
            user_query = arguments["user_query"]
            plot_code = generate_plot_code(user_query, df)
            print({"type": "plot", "content": plot_code})
            return {"type": "plot", "content": plot_code}
        
        elif function_name == "agent_generate_insights":
            arguments = json.loads(function_args)
            user_query = arguments["user_query"]
            function_code = generate_plot_code(user_query, df)
            print(function_code)
            print('\n')
            insights = agent_generate_insights(user_query, df, function_code)
            print({"type": "insights", "content": insights})
            return {"type": "insights", "content": insights}   
        
        elif function_name == "generate_plot_and_insights":
            arguments = json.loads(function_args)
            user_query = arguments["user_query"]
            plot_code = generate_plot_code(user_query, df)
            insights = agent_generate_insights(user_query, df, plot_code)
            print('\n\n')
            print({"type": "plot_and_insights", "content": {"plot": plot_code, "\ninsights": insights}})
            return {"type": "plot_and_insights", "content": {"plot": plot_code, "insights": insights}}
    else:
        return {"type": "error", "content": "No function was called."}
        # return content # Return error message