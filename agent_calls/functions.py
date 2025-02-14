def function_descriptions():
    functions = [
        {
            "name": "generate_plot_code",
            "description": "Generates Python code for plotting based on the provided user query and dataframe. If the user asked for plots only, use this",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_query": {
                        "type": "string",
                        "description": "The user's request for the type of plot to generate.",
                    },
                    "df": {
                        "type": "object",
                        "description": "The dataframe containing the data to be plotted.",
                    }
                },
                "required": ["user_query", "df"],
            },
            "returns": {
                "type": "string",
                "description": "The generated Python code for plotting, enclosed in triple backticks.",
            }
        },
        {
            "name": "agent_generate_insights",
            "description": "Performs data analysis and generates insights/report based on the user query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_query": {
                        "type": "string",
                        "description": "The user's request for the insights or analysis they want.",
                    },
                    "df": {
                        "type": "object",
                        "description": "The dataframe containing the data.",
                    },
                    "function_code": {
                        "type": "object",
                        "description": "The Python code that will be executed to perform analysis.",
                    }
                },
                "required": ["user_query", "df", "function_code"],
            },
            "returns": {
                "type": "string",
                "description": "The insights generated based on the user query and analysis.",
            }
        },
        {
            "name": "generate_plot_and_insights",
            "description": "Generates both a plot and insights based on the user's request. This function combines the functionality of `generate_plot_code` and `agent_generate_insights`.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_query": {
                        "type": "string",
                        "description": "The user's request for generating a plot and insights.",
                    },
                    "df": {
                        "type": "object",
                        "description": "The dataframe containing the data to be plotted and analyzed.",
                    }
                },
                "required": ["user_query", "df"],
            },
            "returns": {
                "type": "object",
                "description": "An object containing both the generated plot code and the insights.",
                "properties": {
                    "plot_code": {
                        "type": "string",
                        "description": "The generated Python code for plotting, enclosed in triple backticks.",
                    },
                    "insights": {
                        "type": "string",
                        "description": "The insights generated based on the user query and analysis.",
                    }
                }
            }
        }
    ]
    return functions