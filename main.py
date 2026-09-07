import streamlit as st

from src.pipeline import (
    run_search_agent,
    run_reader_agent,
    run_writer_agent,
    run_critic_agent,
)


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="",
    layout="wide",
)


# ==========================================
# SESSION STATE
# ==========================================

if "state" not in st.session_state:
    st.session_state.state = {}


# ==========================================
# HEADER
# ==========================================

st.title(" Multi-Agent Research System")

st.caption(
    "Search → Reader → Writer → Critic"
)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("Agent Pipeline")

    st.markdown(
        """
        ###  Search Agent
        Finds relevant information.

        ### Reader Agent
        Reads and extracts deeper context.

        ### Writer Agent
        Creates the research report.

        ### Critic Agent
        Reviews the final report.
        """
    )

    st.divider()

    if st.button("Clear Results"):

        st.session_state.state = {}

        st.rerun()


# ==========================================
# INPUT
# ==========================================

query = st.text_area(
    "What would you like to research?",
    placeholder="Example: How is AI changing software engineering?",
    height=100,
)


# ==========================================
# RUN BUTTON
# ==========================================

if st.button(
    "Start Research",
    use_container_width=True,
):

    if not query.strip():

        st.warning(
            "Please enter a research topic."
        )

        st.stop()


    # ======================================
    # UI COMPONENTS
    # ======================================

    progress_bar = st.progress(0)

    status = st.empty()


    # ======================================
    # CREATE TABS
    # ======================================

    search_tab, reader_tab, writer_tab, critic_tab = st.tabs(
        [
            "Search",
            "Reader",
            "Report",
            "Critic",
        ]
    )


    try:

        # ==================================
        # STEP 1 - SEARCH
        # ==================================

        status.info(
            "Search Agent is researching..."
        )

        with st.spinner(
            "Searching for information..."
        ):

            search_results = run_search_agent(
                query
            )


        st.session_state.state[
            "search_results"
        ] = search_results


        progress_bar.progress(25)


        with search_tab:

            st.success(
                "Search completed!"
            )

            st.markdown(
                search_results
            )


        # ==================================
        # STEP 2 - READER
        # ==================================

        status.info(
            "Reader Agent is analyzing sources..."
        )


        with st.spinner(
            "Reading and scraping sources..."
        ):

            scraped_content = run_reader_agent(
                search_results
            )


        st.session_state.state[
            "scraped_content"
        ] = scraped_content


        progress_bar.progress(50)


        with reader_tab:

            st.success(
                "Reader completed!"
            )

            st.markdown(
                scraped_content
            )


        # ==================================
        # STEP 3 - WRITER
        # ==================================

        status.info(
            "Writer Agent is drafting the report..."
        )


        with st.spinner(
            "Writing final report..."
        ):

            report = run_writer_agent(
                search_results,
                scraped_content,
            )


        st.session_state.state[
            "report"
        ] = report


        progress_bar.progress(75)


        with writer_tab:

            st.success(
                "Report generated!"
            )

            st.markdown(
                report
            )


        # ==================================
        # STEP 4 - CRITIC
        # ==================================

        status.info(
            "Critic Agent is reviewing the report..."
        )


        with st.spinner(
            "Reviewing report..."
        ):

            critic = run_critic_agent(
                report
            )


        st.session_state.state[
            "critic"
        ] = critic


        progress_bar.progress(100)


        with critic_tab:

            st.success(
                "Review completed!"
            )

            st.markdown(
                critic
            )


        # ==================================
        # COMPLETE
        # ==================================

        status.success(
            "Research pipeline completed!"
        )


    except Exception as error:

        status.error(
            f"Pipeline failed: {error}"
        )