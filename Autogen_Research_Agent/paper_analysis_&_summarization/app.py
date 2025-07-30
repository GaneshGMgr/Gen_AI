import streamlit as st
import os
from dotenv import load_dotenv
from agents import ResearchAgents
from data_loader import DataLoader

# Load environment variables
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
image_path = "C:\\Users\\ganes\\DataScience\\Gen_AI\\LangChain\\Course_GenAI\\Gen_AI_In-Depth\\Projects\\Autogen_Research_Agent\\paper_analysis_&_summarization\\media\\logo.png"
# Set up page configuration
st.set_page_config(page_title="Virtual Research Assistant", page_icon="📚", layout="wide")

# Sidebar with branding and input field
st.sidebar.image(image_path, use_container_width=True)
st.sidebar.title("🔍 Research Assistant")
st.sidebar.markdown("Effortlessly find and summarize research papers.")
query = st.sidebar.text_input("Enter a research topic:", placeholder="e.g., Quantum Computing")

# API Key validation
if not groq_api_key:
    st.sidebar.error("GROQ_API_KEY is missing. Please set it in your environment variables.")
    st.stop()

# Initialize AI Agents for summarization and analysis

search_agents = ResearchAgents(groq_api_key) # accessing the self.summarizer_agent, self.advantages_disadvantages_agent and self.search_agent

# search_agents = ResearchAgents() # ollama using
data_loader = DataLoader(search_agent=search_agents.search_agent) # passing the self.search_agent to Dataloader

# Main content area
st.title("📚 Virtual Research Assistant")
st.markdown("Unlock knowledge with AI-powered research analysis!")

if st.sidebar.button("🔍 Search"):
    with st.spinner("Fetching research papers..."):
        arxiv_papers = data_loader.fetch_arxiv_papers(query)
        google_scholar_papers = data_loader.fetch_google_scholar_papers(query)
        all_papers = arxiv_papers + google_scholar_papers

        if not all_papers:
            st.error("No papers found. Try a different topic!")
        else:
            st.success(f"Found {len(all_papers)} research papers!")
            processed_papers = []

            for paper in all_papers:
                summary = search_agents.summarize_paper(paper['summary'])
                adv_dis = search_agents.analyze_advantages_disadvantages(summary)
                processed_papers.append({
                    "title": paper["title"],
                    "link": paper["link"],
                    "summary": summary,
                    "advantages_disadvantages": adv_dis,
                })

            st.subheader("📄 Research Papers")
            for i, paper in enumerate(processed_papers, 1):
                with st.expander(f"{i}. {paper['title']}"):
                    st.markdown(f"**🔗 [Read Paper]({paper['link']})**")
                    st.write(f"**Summary:** {paper['summary']}")
                    st.write(f"**Pros & Cons:** {paper['advantages_disadvantages']}")
                    st.markdown("---")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("Made In Nepal❤️")
