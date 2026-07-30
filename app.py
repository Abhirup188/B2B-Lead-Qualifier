import streamlit as st
import os
import uuid 
from dotenv import load_dotenv
from main import app 
from schemas import AgentState

load_dotenv()

st.set_page_config(page_title="B2B Lead Qualifier AI", page_icon="🚀", layout="wide")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

st.title("🚀 Autonomous B2B Lead Qualifier")
st.caption(f"Session Thread ID: {st.session_state.thread_id}")

with st.sidebar:
    st.header("Settings")
    if st.button("Clear Session Memory"):
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

company_input = st.text_input("Enter Company Name:", placeholder="Stripe")

if st.button("Generate Outreach", type="primary"):
    if not company_input:
        st.warning("Please enter a company name.")
    else:
        initial_state = {"raw_input": company_input, "errors": []}

        config = {"configurable": {"thread_id": st.session_state.thread_id}}
        
        with st.status("Agent processing with Persistence...", expanded=True) as status:
            st.write("🔍 Researching and saving state...")
            final_output = app.invoke(initial_state, config=config)
            status.update(label="Workflow Complete!", state="complete", expanded=False)

        if final_output.get("errors"):
            st.error(f"Error: {final_output['errors'][-1]}")
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.header("📋 Lead Intelligence")
                st.json(final_output.get("lead_data", {}))
            with col2:
                st.header("✉️ Outreach Draft")
                if final_output.get("draft_email"):
                    st.write(final_output["draft_email"]["email_body"])