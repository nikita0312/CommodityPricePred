from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
import os
from dotenv import load_dotenv

load_dotenv(override=True)


# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")


@CrewBase
class Commodai:
    """Commodai crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            verbose=True,
            tool=SerperDevTool(
                n_results=8,
                country="India",
                search_params={
                    "tbs": "qdr:m",  # Limit to past month
                    "sort": "date",  # Sort by date
                    "gl": "in",  # Geolocation set to India
                    "hl": "en",  # Language set to English
                    "num": 10,  # Number of results to fetch
                    "filter": "0",  # Removes duplicate content
                    # "as_rights": "(cc_publicdomain|cc_attribute|cc_sharealike)",  # Look for credible sources
                    "as_sitesearch": "reuters.com OR economictimes.indiatimes.com OR bloomberg.com OR financialexpress.com OR business-standard.com OR livemint.com",  # Limit to reputable sources
                },
            ),
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(config=self.agents_config["reporting_analyst"], verbose=True)

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
        )

    @task
    def reporting_task(self) -> Task:
        return Task(config=self.tasks_config["reporting_task"], output_file="report.md")

    @crew
    def crew(self) -> Crew:
        """Creates the Commodai crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
