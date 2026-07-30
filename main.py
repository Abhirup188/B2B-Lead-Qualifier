import os
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from schemas import LeadInfo  
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(model="gpt-5-nano-2025-08-07", temperature=0) 
tavily_tool = TavilySearchResults(max_results=4)

def researcher_node(state: dict) -> dict:
    """
    Takes the raw company name, searches the web, and forces the LLM 
    to extract the data into our strict LeadInfo schema.
    """
    company = state.get("raw_input")
    
    if not company:
        return {"errors": ["Critical: No company name provided in AgentState."]}
        
    print(f"--- RESEARCHING: {company} ---")
    
    try:
        search_query = f"{company} company overview, software tech stack, and recent business news"
        search_results = tavily_tool.invoke({"query": search_query})
        
        context = "\n\n".join([f"Source: {res['url']}\nContent: {res['content']}" for res in search_results])
        extractor_llm = llm.with_structured_output(LeadInfo)
        
        prompt = f"""
        You are an expert B2B research assistant. 
        Analyze the following search results about the company '{company}'.
        Extract the company name, industry, tech stack, and any current pain points or recent news.
        If you cannot find specific tech stack details, infer based on their industry, but keep it realistic.
        
        Context:
        {context}
        """

        structured_lead_data = extractor_llm.invoke(prompt)

        return {"lead_data": structured_lead_data.model_dump()}
        
    except Exception as e:
        print(f"--- RESEARCH FAILED: {e} ---")
        return {"errors": [f"Research step failed: {str(e)}"]}
    

from langgraph.graph import END
from schemas import Evaluation 

def evaluator_node(state: dict) -> dict:
    """
    The Gatekeeper. Scores the lead against the ICP and outputs a strict boolean.
    """
    print("--- EVALUATING LEAD FIT ---")

    if "errors" in state and state["errors"]:
        print("Bypassing evaluation due to upstream errors.")
        return {"evaluation": {"score": 0, "is_qualified": False, "reasoning": "Upstream research failed."}}
        
    lead = state.get("lead_data")
    if not lead:
        return {"errors": ["Critical: No lead data available for evaluation."]}

    icp_definition = """
    Ideal Customer Profile (ICP):
    - Target: B2B Software, SaaS, or Tech-enabled services.
    - Tech Stack: Must be using modern web frameworks (React, Vue, Angular) or backend languages (Python, Node.js).
    - Pain Points: Look for signs of scaling, hiring engineers, or modernizing infrastructure.
    
    Disqualify if:
    - They are a local mom-and-pop shop (e.g., local bakery, plumbing).
    - They solely use legacy enterprise software without signs of modernization.
    """

    evaluator_llm = llm.with_structured_output(Evaluation)
    
    prompt = f"""
    You are a ruthless B2B Lead Qualifier. 
    Analyze the following company data against the Ideal Customer Profile (ICP).
    
    Company Data:
    {lead}
    
    {icp_definition}
    
    Calculate a fit score (0-100). If the score is > 70, is_qualified is True. Otherwise, False.
    Provide a 1-sentence brutally honest reasoning.
    """
    
    try:
        evaluation_result = evaluator_llm.invoke(prompt)
        return {"evaluation": evaluation_result.model_dump()}
    except Exception as e:
        print(f"--- EVALUATION FAILED: {e} ---")
        return {"errors": [f"Evaluation step failed: {str(e)}"]}


def should_continue(state: dict) -> str:
    """
    Reads the state and determines the next node. 
    Returns the exact string name of the node to route to.
    """
    if "errors" in state and state["errors"]:
        return "end"
        
    evaluation = state.get("evaluation", {})
    
    if evaluation.get("is_qualified"):
        print(">> Lead Qualified. Routing to Copywriter...")
        return "continue"
    else:
        print(">> Lead Disqualified. Terminating workflow.")
        return "end"
    
from schemas import OutreachDraft

def copywriter_node(state: dict) -> dict:
    """
    Drafts a hyper-personalized cold email based ONLY on the validated research.
    """
    print("--- GENERATING OUTREACH DRAFT ---")
    
    lead = state.get("lead_data", {})
    evaluation = state.get("evaluation", {})
    
    writer_llm = llm.with_structured_output(OutreachDraft)
    
    prompt = f"""
    You are an elite B2B technical copywriter. 
    Write a highly personalized, concise cold email to the decision-maker at {lead.get('company_name')}.
    
    Company Context:
    - Industry: {lead.get('industry')}
    - Tech Stack: {', '.join(lead.get('tech_stack', []))}
    - Pain Points/Recent News: {', '.join(lead.get('pain_points', []))}
    
    Why we are targeting them (Our internal reasoning): 
    {evaluation.get('reasoning')}
    
    Strict Rules:
    1. Maximum 4 sentences.
    2. Explicitly mention one of their specific technologies or recent news items in the first sentence.
    3. Do not use generic buzzwords (e.g., "synergy", "paradigm shift"). 
    4. Keep the tone professional but brutally direct.
    """
    
    try:
        draft = writer_llm.invoke(prompt)
        return {"draft_email": draft.model_dump()}
    except Exception as e:
        print(f"--- COPYWRITING FAILED: {e} ---")
        return {"errors": [f"Copywriter step failed: {str(e)}"]}
    
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from schemas import AgentState 

memory=MemorySaver()

workflow = StateGraph(AgentState)

workflow.add_node("researcher", researcher_node)
workflow.add_node("evaluator", evaluator_node)
workflow.add_node("copywriter", copywriter_node)

workflow.set_entry_point("researcher")

workflow.add_edge("researcher", "evaluator")

workflow.add_conditional_edges(
    "evaluator",
    should_continue,
    {
        "continue": "copywriter",
        "end": END
    }
)

workflow.add_edge("copywriter", END)

app = workflow.compile(checkpointer=memory)

if __name__ == "__main__":
    test_company = "Vercel"
    initial_state = {"raw_input": test_company}

    config = {"configurable": {"thread_id": "test_lead_001"}}
    
    final_state = app.invoke(initial_state, config=config)
    
    print("\n=== PERSISTENT STATE SAVED ===")
    import json
    print(json.dumps(final_state, indent=2))