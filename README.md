Autonomous B2B Lead Qualification Agent

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-Enabled-green.svg)](https://langchain.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-orange.svg)](https://langchain.com/langgraph)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-red.svg)](https://streamlit.io/)

An intelligent, multi-agent AI system designed to automate B2B lead enrichment, qualification, and scoring. Built using LangGraph and Python, this system replaces hours of manual pipeline research by autonomously profiling companies, identifying pain points, and scoring lead viability in seconds.

The Problem vs. The Solution

The Problem: Sales and marketing teams spend up to 40% of their day manually researching target companies, evaluating if they fit the Ideal Customer Profile (ICP), and writing personalized outreach contexts.
The Solution: This AI agent swarm ingests raw lead data (URL or company name) and autonomously executes a multi-step research and qualification workflow, outputting a highly structured executive summary and lead score.

Architecture & Workflow

This project utilizes a LangGraph State Machine to orchestrate specialized AI agents:

1. Researcher Agent: Scrapes and parses the target company's web presence and recent news.
2. Profiler Agent: Extracts core business metrics (industry, target audience, value proposition).
3. Qualification Agent: Compares the company profile against a predefined ICP and assigns a Lead Score (0-100).
4. Strategist Agent: Drafts personalized outreach hooks and identifies potential business bottlenecks.
5. Supervisor Node: Reviews the output for formatting and accuracy before compiling the final JSON/Markdown report.

Tech Stack

Core Logic: Python
* LLM Orchestration: LangChain & LangGraph
* Frontend/UI: Streamlit (for interactive web dashboard)
* Data Handling: Pandas
* Web Scraping/Search: Tavily API / BeautifulSoup (Optional based on configuration)

Quick Start & Installation

1. Clone the repository
```bash
git clone [https://github.com/yourusername/b2b-lead-qualifier.git](https://github.com/yourusername/b2b-lead-qualifier.git)
cd b2b-lead-qualifier
```
2. Set up a virtual environment (Recommended)
```Bash
python -m venv venv
source venv/Scripts/activate
```
3. Configure Environment Variables
Create a .env file in the root directory and add your API keys:

Code snippet
```bash
OPENAI_API_KEY=your_openai_key_here
TAVILY_API_KEY=your_tavily_key_here
```


4. Run the Application
```Bash
streamlit run app.py
```
Example Output
When a lead URL is processed, the agentic swarm generates:

Company Overview: (Size, Sector, Core Product)

ICP Match Score: 85/100

Key Pain Points: (e.g., "Manual data entry overhead," "High customer acquisition cost")

Suggested Outreach Angle: (A highly targeted 2-sentence hook for cold email)

Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

Author
Abhirup Chakraborty

Multi-Agent AI Architect & Data Systems Developer

Connect on LinkedIn

License
MIT
