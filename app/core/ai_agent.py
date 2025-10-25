from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

def get_response_from_ai_agents(llm_id, query, allow_search, system_prompt):
    try:
        # Initialize LLM
        llm = ChatGroq(model=llm_id, api_key=settings.GROQ_API_KEY)

        # Initialize tools
        tools = []
        if allow_search:
            tavily_tool = TavilySearchResults(
                max_results=2,
                api_key=settings.TAVILY_API_KEY,
                name="tavily_search",
                description="Search the web for current information"
            )
            tools.append(tavily_tool)

        # Create agent using LangGraph
        agent_executor = create_react_agent(llm, tools)

        # Prepare the input
        # Combine system prompt and user query
        full_query = f"{system_prompt}\n\nUser Query: {' '.join(query)}"
        
        # Run the agent
        result = agent_executor.invoke({"messages": [("user", full_query)]})
        
        # Extract the final response
        messages = result.get("messages", [])
        if messages:
            # Get the last AI message
            final_message = messages[-1]
            return final_message.content
        
        return "No response from AI agent."

    except Exception as e:
        logger.exception("Error while generating response from AI agent")
        raise CustomException("Failed to get response from AI agent", e)