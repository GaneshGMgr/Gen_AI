import os
from autogen import AssistantAgent
from data_loader import DataLoader
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ResearchAgents:
    def __init__(self, api_key):
        self.groq_api_key = api_key
        self.llm_config = {'config_list': [{'model': 'llama-3.3-70b-versatile', 'api_key': self.groq_api_key, 'api_type': "groq"}]}

    # def __init__(self):
    #     self.llm_config = {
    #         'config_list': [
    #             {'model': 'llama3:latest', 'api_type': "ollama"}  # Using the locally downloaded model
    #         ]
    #     }

        # Summarizer Agent - Summarizes research papers
        self.summarizer_agent = AssistantAgent(
            name="summarizer_agent",
            system_message="Summarize the retrieved research papers and present concise summaries to the user, JUST GIVE THE RELEVANT SUMMARIES OF THE RESEARCH PAPER AND NOT YOUR THOUGHT PROCESS.",
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            code_execution_config=False
        )

        # Advantages and Disadvantages Agent - Analyzes pros and cons
        self.advantages_disadvantages_agent = AssistantAgent(
            name="advantages_disadvantages_agent",
            system_message="Analyze the summaries of the research papers and provide a list of advantages and disadvantages for each paper in a pointwise format. JUST GIVE THE ADVANTAGES AND DISADVANTAGES, NOT YOUR THOUGHT PROCESS",
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            code_execution_config=False
        )

        # If you plan to use a search agent to suggest related topics, you need to initialize it
        self.search_agent = AssistantAgent(
            name="search_agent",
            system_message="Suggest 3 related research topics for a given query.",
            llm_config=self.llm_config,
            human_input_mode="NEVER",
            code_execution_config=False
        )


    def summarize_paper(self, paper_summary):
        """Generates a summary of the research paper."""
        summary_response = self.summarizer_agent.generate_reply(
            messages=[{"role": "user", "content": f"Summarize this paper: {paper_summary}"}]
        )
        return summary_response.get("content", "Summarization failed!") if isinstance(summary_response, dict) \
                else str(summary_response)

    def analyze_advantages_disadvantages(self, paper_summary):
        """Analyzes advantages and disadvantages of the research paper."""
        adv_dis_response = self.advantages_disadvantages_agent.generate_reply(
            messages=[{"role": "user", "content": f"Analyze advantages and disadvantages of this paper: {paper_summary}"}]
        )
        return adv_dis_response.get("content", "Analysis failed!") if isinstance(adv_dis_response, dict) else str(adv_dis_response)
