from agents import CreateSearchAgent, CreateReaderAgent, writer_chain, critic_chain

def run_search_pipeline(query: str):
    """Run the multi-agent system one after another"""
    state = {}
    print("\n", "="*50)
    print("Search agent working...")
    
 
    search_results = CreateSearchAgent().invoke({
        "messages": [
            {
                "role": "user",
                "content": f"{query}",
            }
        ]
    })
    
    state['search_results'] = search_results['messages'][-1].content
    print("\nSEARCH RESULTS:\n", state['search_results'])
    
    
    print("\n", "="*50)
    print("Reader agent working...")
    
    scraped_content = CreateReaderAgent().invoke({
        "messages": [
            {
                "role": "user",
                "content": f"{state['search_results']}",
            }
        ]
    })
    
    state['scraped_content'] = scraped_content['messages'][-1].content
    print("\nSCRAPED CONTENT: \n", state['scraped_content'])
    
    print("\n", "="*50)
    print("Writer agent working...")
    
    combined_report = (
    f"Search Results: {state['search_results']}"
    f"Scraped Content: {state['scraped_content']}"
)
    
    final_draft = writer_chain.invoke({"research": combined_report})
    state['report'] = final_draft
    print("\nFINAL REPORT:\n", state['report'])
    
    print("\n", "="*50)
    print("Critic agent working...")
    
    critic = critic_chain.invoke({"report": state['report']})
    state['critic'] = critic
    print("\nREVIEW: \n", state['critic'])
    
    return state
    
    