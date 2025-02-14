# AI-Powered Data Analyst Application

## Overview
This project is an AI-powered data analyst application that allows users to upload datasets, describe their visualization or analysis needs in natural language, and receive generated visualizations and insights. The application leverages OpenAI's GPT models to interpret user requests, generate Python code for plotting or analysis, and execute the code to produce results.

The application is built with a modular architecture, separating the backend logic (agents for routing, code generation, and insights) from the frontend interface (Streamlit for the user interface).


https://github.com/user-attachments/assets/54c5af67-e676-4b9f-acff-13dd5921af66



---

## Directory Structure
The project is organized as follows:

```
.env                             # Store apis keys
src/
├── agent_router/
│   ├── routing_agent.py         # Routes user requests to the appropriate plotting or insights functions.
│   └── prompt_agent_router.py   # Contains prompt templates for determining request types.
├── agent_calls/
│   └── functions.py             # Defines API functions and metadata for calling analysis components.
├── agent_generate_plot_code/
│   ├── generate_plots.py        # Generates Python code for creating visualizations based on user requests.
│   └── prompts.py               # Contains prompt templates used for plot code generation.
├── agent_generate_insights/
│   ├── generate_insights.py     # Generates analytical insights based on dataset metrics.
│   └── prompts.py               # Contains prompt templates used for insight code generation.
└── frontend/
    └── app.py                 # Streamlit UI for uploading data, entering requests, and displaying output.
requirements.txt              # Lists external Python libraries and dependencies.
```

---

## Components

### 1. **Agent Router (`agent_router/`)**
- **`routing_agent.py`**: Routes user requests to the appropriate function (plot generation or insights generation) based on the input query.
- **`prompt_agent_router.py`**: Contains the prompt used by the routing agent to determine the type of request (plot or insights).

### 2. **Agent Calls (`agent_calls/`)**
- **`functions.py`**: Defines the function descriptions and metadata used by the routing agent to call the appropriate functions.

### 3. **Plot Generation (`agent_generate_plot_code/`)**
- **`generate_plots.py`**: Generates Python code for creating visualizations based on user requests. It uses OpenAI's GPT models to interpret the request and generate the corresponding code.

### 4. **Insights Generation (`agent_generate_insights/`)**
- **`generate_insights.py`**: Generates insights and analysis based on the computed values from the dataset. It uses OpenAI's GPT models to provide actionable insights.

### 5. **Frontend (`frontend/`)**
- **`app.py`**: The Streamlit-based frontend application. It allows users to upload datasets, enter their requests, and view the generated visualizations and insights.

---

## How It Works

### Workflow
1. **User Uploads Data**:
   - The user uploads a dataset (CSV or Excel) through the Streamlit interface.
2. **User Describes Request**:
   - The user describes their visualization or analysis needs in natural language (e.g., "Plot sales over time" or "Analyze sales trends").
3. **Routing Agent**:
   - The routing agent interprets the user's request and determines whether to generate a plot or insights.
4. **Code Execution**:
   - If the request is for a plot, the application generates and executes Python code to create the visualization.
   - If the request is for insights, the application computes the necessary metrics and generates a textual analysis.
5. **Output Display**:
   - The results (plots or insights) are displayed in the Streamlit interface.

---

## Features

### 1. **Natural Language Processing**
- Users can describe their visualization or analysis needs in plain English.
- The application uses OpenAI's GPT models to interpret the requests and generate the corresponding code or insights.

### 2. **Dynamic Plot Generation**
- The application generates Python code for creating visualizations (e.g., line plots, bar charts) based on user requests.
- The generated code is executed dynamically to produce the plots.

### 3. **Actionable Insights**
- The application provides insights and analysis based on the dataset and user requests.
- Insights are generated using OpenAI's GPT models and are displayed in a user-friendly format.

### 4. **Streamlit Frontend**
- The frontend is built using Streamlit, providing a clean and interactive interface for users.
- Users can upload datasets, enter requests, and view results in real-time.

---

## Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key (set as an environment variable `OPENAI_API_KEY`)
- Required Python libraries (install via `pip install -r requirements.txt`)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ai-powered-analyst.git
   cd ai-powered-analyst
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your-api-key"
   ```
4. Run the Streamlit app:
   ```bash
   streamlit run src/frontend/app.py
   ```

---

## Usage

1. **Upload Dataset**:
   - Use the file uploader to upload a CSV or Excel file.
2. **Enter Request**:
   - Describe your visualization or analysis needs in the text area (e.g., "Plot sales over time" or "Analyze sales trends").
3. **Generate Results**:
   - Click the "Generate" button to process your request.
4. **View Output**:
   - The application will display the generated visualization or insights, along with a summary of the dataset.

---

## Example Requests

### Visualization Requests
- "Plot sales over time."
- "Create a bar chart of total sales by product."
- "Show a histogram of customer ages."

### Analysis Requests
- "Analyze sales trends over the past year."
- "Identify the top 5 products by sales."
- "Compare sales performance between regions."

---

## Acknowledgments
- OpenAI for providing the GPT models.
- Streamlit for the easy-to-use frontend framework.
- Pandas, Matplotlib, and Seaborn for data manipulation and visualization.

---

