# 🤖 AI-Powered Data Analyst

An end-to-end AI application that lets anyone upload a dataset and instantly get automated analysis, ask questions in plain English, and generate professional business reports.

## 💡 What It Does
- 📊 **Auto Analysis** — Instant EDA, stats, charts, and correlation heatmaps
- 💬 **Ask Your Data** — Type questions in plain English, AI writes and runs the code
- 📄 **Generate Report** — Professional consulting-style business insights report
- 📥 **PDF Export** — Download your report instantly

## 🛠️ Tech Stack
- **LLM** — Groq (LLaMA 3.3 70B) for natural language understanding
- **Frontend** — Streamlit
- **Data Processing** — Pandas, Matplotlib, Seaborn
- **PDF Generation** — FPDF2
- **Language** — Python 3.14

## ⚙️ How to Run Locally
1. Clone the repo
2. Create virtual environment and activate it
3. Run `pip install -r requirements.txt`
4. Add your Groq API key in a `.env` file as `GROQ_API_KEY=your-key`
5. Run `streamlit run app.py`

## 🎯 Use Cases
- Business analysts exploring new datasets
- Data scientists doing quick EDA
- Managers who need instant reports without coding
- Anyone who wants to understand their data using plain English

## 👨‍💻 Author
Atharva — https://github.com/Atharva-Dem