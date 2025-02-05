import streamlit as st
import httpx
import json
import plotly.graph_objects as go
from datetime import datetime
import time

# Configure the page
st.set_page_config(
    page_title="LLM Honeypot System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
API_URL = "http://127.0.0.1:8000"

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1E1E1E 0%, #2D2D2D 100%);
        color: white;
    }
    div[data-testid="stToolbar"] {
        display: none;
    }
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.2);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    section[data-testid="stSidebar"] > div {
        color: white;
    }
    .stTextInput input, .stSelectbox select, .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    .stTextInput label, .stSelectbox label, .stTextArea label {
        color: white !important;
    }
    .stButton > button {
        background-color: #FF4B4B;
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 0.5rem;
    }
    .stButton > button:hover {
        background-color: #FF3333;
    }
    div[data-testid="stMarkdown"] {
        color: white;
    }
    h1, h2, h3, h4, h5, h6, p {
        color: white !important;
    }
    .metric-container {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 0.5rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF4B4B !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for error handling
if 'error_message' not in st.session_state:
    st.session_state.error_message = None

def get_system_status():
    """Get system status from the API"""
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(f"{API_URL}/status")
            if response.status_code == 200:
                st.session_state.error_message = None
                return response.json()
            else:
                st.session_state.error_message = f"API Error: {response.status_code}"
                return None
    except Exception as e:
        st.session_state.error_message = f"Connection Error: Could not connect to API server"
        return None

def process_agent_request(agent: str, data: dict):
    """Send request to specific agent"""
    try:
        with httpx.Client(timeout=30.0) as client:  
            response = client.post(
                f"{API_URL}/process",
                json={"agent": agent, "data": data}
            )
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"API returned status code: {response.status_code}")
    except httpx.TimeoutException:
        st.error("Request timed out. The agent is taking longer than expected to respond.")
        return None
    except httpx.ConnectError:
        st.error("Could not connect to the API server. Please make sure it's running.")
        return None
    except Exception as e:
        st.error(f"Error processing request: {str(e)}")
        return None

def analyze_threat(data: dict):
    """Send threat analysis request"""
    try:
        with httpx.Client() as client:
            response = client.post(f"{API_URL}/analyze", json=data)
            return response.json()
    except Exception as e:
        st.error(f"Error analyzing threat: {str(e)}")
        return None

# Sidebar with error handling
st.sidebar.title("🎯 LLM Honeypot")
st.sidebar.markdown("---")

# System Status with improved error display
status = get_system_status()
if status:
    st.sidebar.success("✅ System Online")
    for agent, state in status["agent_status"].items():
        st.sidebar.markdown(f"**{agent.title()}**: _{state}_")
else:
    st.sidebar.error("❌ System Offline")
    if st.session_state.error_message:
        st.sidebar.warning(st.session_state.error_message)
        st.sidebar.info("Make sure the API server is running on port 8000")

# Main content
st.title("LLM Honeypot System")
st.markdown("---")

# Tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["Agent Interaction", "Threat Analysis", "System Metrics"])

with tab1:
    st.header("Agent Interaction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_agent = st.selectbox(
            "Select Agent",
            ["architect", "llm_specialist", "honeypot_expert", 
             "security_analyst", "infrastructure_engineer", "data_scientist"]
        )
        
        task_input = st.text_area("Task Description")
        
        if st.button("Process Task"):
            if task_input:
                with st.spinner("Processing... This may take a few seconds"):
                    result = process_agent_request(
                        selected_agent,
                        {"task": task_input}
                    )
                    if result:
                        st.success("Task processed successfully!")
                        with st.expander("View Response", expanded=True):
                            st.json(result)
            else:
                st.warning("Please enter a task description")

with tab2:
    st.header("Threat Analysis")
    
    threat_data = st.text_area("Threat Data (JSON format)")
    
    if st.button("Analyze Threat"):
        if threat_data:
            try:
                data = json.loads(threat_data)
                with st.spinner("Analyzing threat..."):
                    result = analyze_threat(data)
                    if result:
                        st.json(result)
            except json.JSONDecodeError:
                st.error("Invalid JSON format")
        else:
            st.warning("Please enter threat data")

with tab3:
    st.header("System Metrics")
    
    # Mock metrics for demonstration
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Active Threats", "5", "+2")
    
    with col2:
        st.metric("Response Time", "124ms", "-12ms")
    
    with col3:
        st.metric("System Load", "42%", "+5%")
    
    # Mock threat detection graph
    fig = go.Figure()
    
    # Add mock data
    times = [datetime.now().strftime("%H:%M:%S") for _ in range(10)]
    values = [3, 5, 4, 6, 7, 5, 4, 6, 8, 7]
    
    fig.add_trace(go.Scatter(
        x=times,
        y=values,
        mode='lines+markers',
        name='Threats Detected'
    ))
    
    fig.update_layout(
        title="Threat Detection Timeline",
        xaxis_title="Time",
        yaxis_title="Number of Threats",
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
