from app.core.model import ResumeData, PersonalInfo, Education, SkillItem, Experience, Project
from app.core.LatexFunction import render
from app.core.LatexTemplate import generate_latex

resume_data = ResumeData(
        personal_info=PersonalInfo(
            full_name="remoon",
            phone="+1-934-246-4678",
            email="sethuramgautha.rajakumar@stonybrook.edu",
            linkedin_url="https://www.linkedin.com/in/sethuram-gautham-r-851733205/",
            linkedin_disp_name="Sethuram",
            github_url="https://github.com/Sethuram2003",
            github_disp_name="Sethuram2003"
        ),
        education=[
            Education(
                institution="Stony Brook University",
                location="New York, United States",
                degree="Masters of Science in Data Science",
                gpa="3.67",
                date_range="August 2024 - May 2026",
                courses=["Data Analysis", "Probability", "Statistical Learning", "Statistical Computing", 
                        "Data Structures and Algorithms", "Data Management", "Cloud Computing", "Big Data Analysis"]
            ),
            Education(
                institution="SSN College of Engineering",
                location="Chennai, India",
                degree="Bachelor of Engineering in Electrical and Electronics Engineering",
                gpa="8.8",
                date_range="June 2020 - May 2024",
                courses=["Problem Solving and Programming in Python", "Object Oriented Programming(Java)", 
                        "Linear Algebra and Calculus"]
            )
        ],
        skills=[
            SkillItem(
                category="Programming Languages",
                items=["Python", "Shell (Bash)", "C++", "SQL", "Java", "R"]
            ),
            SkillItem(
                category="Database Technologies",
                items=["Amazon Redshift", "MySQL", "CosmosDB", "HDFS", "HBase", "PostgreSQL", 
                      "Vector Database", "MongoDB", "Cassandra", "Snowflake", "neo4j"]
            ),
            SkillItem(
                category="Big Data Tools",
                items=["Apache Spark", "Hadoop", "Kafka", "Hive", "Airflow", "Databricks", "Flink", "docker"]
            ),
            SkillItem(
                category="LLM & AI Tools",
                items=["Ollama", "Hugging Face Transformers", "Langchain", "Letta", "Swarm", 
                      "OpenAI GPT", "LlamaIndex", "Pinecone", "Weaviate", "langflow", "n8n"]
            )
        ],
        experience=[
            Experience(
                title="Associate Software Engineer - Intern",
                location="New York, New York, USA",
                company="HGS Digital",
                date_range="May 2025 - Jan 2026",
                highlights=[
                    "Designed and deployed scalable AI voice agents and full-stack automation systems across healthcare, finance, and customer support, enabling real-time interactions, autonomous decision-making, and significant reductions in manual workflows using Azure Cloud Functions",
                    "Architect-ed multi-agent AI workflows by fine-tuning language models and orchestrating MCP servers, LangGraph, LangFlow, and n8n, delivering high-performance, production-ready automation with improved response times, reliability, and operational efficiency."
                ]
            )
        ],
        projects=[
            Project(
                name="Local RAG Application for Document Retrieval and Question Answering",
                affiliation="Self-Initiated Project",
                date_range="February 2025 - Present",
                description=[
                    "Developed a Retrieval-Augmented Generation (RAG) application locally using DeepSeek, Sentence Transformers, and Ollama, enabling efficient document retrieval and context-aware question answering with 95% accuracy.",
                    "Designed and deployed the entire system on a local machine, optimizing resource utilization and ensuring secure, offline functionality for sensitive data applications."
                ]
            ),
            Project(
                name="AdaptiMind: Context-Aware AI Agent with Dynamic Memory",
                affiliation="Self-Initiated Project",
                date_range="January 2025 - Present",
                description=[
                    "Designed a stateful agent on the Letta platform using Llama 3.1 as its conversational core, integrating custom tools for task execution and enabling real-time, context-aware solutions tailored to user needs.",
                    "Implemented dynamic learning and memory update capabilities, allowing the agent to evolve through user interactions, improving response accuracy of personal information by 90% and delivering a personalized, adaptive experience locally."
                ]
            )
        ]
    )

LATEX_TEMPLATE = generate_latex(resume_data)

print(render(LATEX_TEMPLATE))