# query_engine.py
# This file takes your plain English question,
# sends it to GPT-4o, gets Python code back,
# runs that code on your data, and returns the result

# query_engine.py
import os
from groq import Groq
from dotenv import load_dotenv
import matplotlib.pyplot as plt

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def query_dataframe(df, user_question):

    df_info = f"""
    The dataframe variable is called 'df'.
    Column names: {list(df.columns)}
    Data types of each column: {df.dtypes.to_dict()}
    First 3 rows of data: {df.head(3).to_string()}
    """

    prompt = f"""
    You are a Python and Pandas expert.

    Here is information about the dataframe:
    {df_info}

    Write ONLY executable Python code (no explanation, no markdown, no backticks)
    to answer this question: {user_question}

    Important rules:
    - Always use 'df' as the dataframe variable name
    - Store your final answer in a variable called 'result'
    - If the answer is a chart, use matplotlib, store the figure in 'fig'
    - Keep the code simple and correct
    - Do not import pandas or matplotlib — they are already available
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    code = response.choices[0].message.content.strip()
# Remove markdown backticks if AI adds them
    if code.startswith("```"):
        code = code.split("\n", 1)[-1]  # remove first line (```python)
    if code.endswith("```"):
        code = code.rsplit("```", 1)[0]  # remove last ```
    code = code.strip()

    local_vars = {"df": df.copy(), "plt": plt}

    try:
        exec(code, {}, local_vars)
        result = local_vars.get("result", None)
        fig = local_vars.get("fig", None)
        return code, result, fig, None

    except Exception as e:
        return code, None, None, str(e)