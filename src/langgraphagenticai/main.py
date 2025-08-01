import streamlit as st

from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit


def load_langgraph_agentic_ai_app():
    """
    Loads and runs the LangGraph AgenticAI application with Streamlit UI. This function initializes the UI, handles user input, configures the LLM model, sets up the graph based on the selected use case, and displays the output while implementing exception handling for robustness.
    """
    
    # Load UI
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()
    
    if not user_input:
        st.error("Error: User input is missing. Please try again.")
        return
    
    user_message = st.chat_input("Enter your message:")
    
    if user_message:
        try:
            ## Configure LLM Model
            obj_llm_config = GroqLLM(user_controls_input=user_input)
            model = obj_llm_config.get_llm_model()
            
            if not model :
                st.error("Error: LLM Model is missing. Please try again.")
                return
            
            # Initialize and setup the graph based on the use case
            usecase = user_input.get("selected_usecase")
            
            if not usecase :
                st.error("Error: No use case selected. Please try again.")
                return
            
            ## Graph Builder
            
            graph_builder = GraphBuilder(model)
            try :
                graph = graph_builder.setup_graph(usecase)
                DisplayResultStreamlit(usecase, graph, user_message).display_result_on_ui()
            
            except Exception as e :
                st.error(f"Error : Graph setup failed : {e}")
                return
                
            
        except Exception as e:
            st.error(f"Error : Graph setup failed : {e}")
            return