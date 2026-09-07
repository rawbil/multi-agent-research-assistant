from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from tools import tavily, scrape_url

load_dotenv()

if "GROQ_API_KEY" not in os.environ:
    raise ValueError("GROQ API key missing")
    
if "TAVILY_API_KEY" not in os.environ:
    raise ValueError("Tavily API key missing")
    
groq_api_key = os.getenv("GROQ_API_KEY")



llm = ChatGroq(model="openai/gpt-oss-safeguard-20b")


def CreateSearchAgent():
    """Search over the internet and return at least 5 sources of information"""
    
    search_agent = create_agent(
        model=llm,
        tools=[tavily],
        system_prompt="You are a professional researcher. Given a topic, traverse the internet and return the most factual sources. The information should be in string format(No Markdown). It should contain the results, and the url of each result. The urls should be structured such that they can be extracted later",
        # response_format=ToolStrategy(Answer)
    )

    return search_agent


def CreateReaderAgent():
    """Scrape a single source and return a detailed report"""
    
    reader_agent = create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt=(
            "You are a web research reader. You MUST call scrape_url before writing your answer. "
            "Choose one URL from the supplied URLs, call scrape_url with that exact URL, and base "
            "your report on the returned page content. Never answer from the search results alone. "
            "After the tool returns, provide the final report as plain text."
        ),
        # response_format=ToolStrategy(Results)
    )
    return reader_agent



writer_prompt = ChatPromptTemplate(
    [
        (
            "system",
            "You are a skilled research assistant. Given a report, form a detailed formal report about it."
            """The report should include the sources, detailed explanations and overview""",
        ),
        (
            "human",
            """Write a detailed research report on the topic below.
        
                    Research Gathered:
                    {research}
        
                    Structure the report as:
                    - Introduction
                    - Key Findings (minimum 3 well-explained points)
                    - Conclusion
                    - Sources (list all URLs found in the research)
        
                    Be detailed, factual and professional.
                    """,
        ),
    ]
)

writer_chain = writer_prompt | llm | StrOutputParser()


critic_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a sharp and constructive research critic. Be honest and specific.",
        ),
        (
            "human",
            """Review the research report below and evaluate it strictly.

        Report:
        {report}

        Respond in this exact format:

        Score: X/10

        Strengths:
        - ...
        - ...

        Areas to Improve:
        - ...
        - ...

        One line verdict:
        ...""",
        ),
    ]
)

critic_chain = critic_prompt | llm | StrOutputParser()
