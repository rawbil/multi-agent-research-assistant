# from .agents import CreateSearchAgent, CreateReaderAgent, writer_chain, critic_chain

# def run_search_pipeline(query: str):
#     """Run the multi-agent system one after another"""
#     state = {}
#     print("\n", "="*50)
#     print("Search agent working...")
    
 
#     search_results = CreateSearchAgent().invoke({
#         "messages": [
#             {
#                 "role": "user",
#                 "content": f"{query}",
#             }
#         ]
#     })
    
#     state['search_results'] = search_results['messages'][-1].content
#     print("\nSEARCH RESULTS:\n", state['search_results'])
    
    
#     print("\n", "="*50)
#     print("Reader agent working...")
    
#     scraped_content = CreateReaderAgent().invoke({
#         "messages": [
#             {
#                 "role": "user",
#                 "content": f"{state['search_results']}",
#             }
#         ]
#     })
    
#     state['scraped_content'] = scraped_content['messages'][-1].content
#     print("\nSCRAPED CONTENT: \n", state['scraped_content'])
    
#     print("\n", "="*50)
#     print("Writer agent working...")
    
#     combined_report = (
#     f"Search Results: {state['search_results']}"
#     f"Scraped Content: {state['scraped_content']}"
# )
    
#     final_draft = writer_chain.invoke({"research": combined_report})
#     state['report'] = final_draft
#     print("\nFINAL REPORT:\n", state['report'])
    
#     print("\n", "="*50)
#     print("Critic agent working...")
    
#     critic = critic_chain.invoke({"report": state['report']})
#     state['critic'] = critic
#     print("\nREVIEW: \n", state['critic'])
    
#     return state
    
    

from .agents import (
    CreateSearchAgent,
    CreateReaderAgent,
    writer_chain,
    critic_chain,
)


def run_search_agent(query: str) -> str:
    """Run the Search Agent."""

    search_results = CreateSearchAgent().invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": query,
                }
            ]
        }
    )

    return search_results["messages"][-1].content


def run_reader_agent(search_results: str) -> str:
    """Run the Reader Agent."""

    scraped_content = CreateReaderAgent().invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": search_results,
                }
            ]
        }
    )

    return scraped_content["messages"][-1].content


def run_writer_agent(
    search_results: str,
    scraped_content: str,
):
    """Run the Writer Agent."""

    combined_report = f"""
SEARCH RESULTS:
{search_results}

SCRAPED CONTENT:
{scraped_content}
"""

    final_draft = writer_chain.invoke(
        {
            "research": combined_report
        }
    )

    return final_draft


def run_critic_agent(report: str):
    """Run the Critic Agent."""

    critic = critic_chain.invoke(
        {
            "report": report
        }
    )

    return critic


def run_search_pipeline(query: str):
    """Run the complete multi-agent pipeline."""

    state = {}

    # ----------------------------------------
    # SEARCH AGENT
    # ----------------------------------------

    state["search_results"] = run_search_agent(query)


    # ----------------------------------------
    # READER AGENT
    # ----------------------------------------

    state["scraped_content"] = run_reader_agent(
        state["search_results"]
    )


    # ----------------------------------------
    # WRITER AGENT
    # ----------------------------------------

    state["report"] = run_writer_agent(
        state["search_results"],
        state["scraped_content"],
    )


    # ----------------------------------------
    # CRITIC AGENT
    # ----------------------------------------

    state["critic"] = run_critic_agent(
        state["report"]
    )

    return state
    