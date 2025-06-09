from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.agents import Tool, initialize_agent, AgentType
from tools import scrape_blog_content, generate_podcast_audio
import os

# === Gemini Setup ===
os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)

# === Prompt Setup ===
with open("prompts/podcast_prompt.txt") as f:
    prompt_text = f.read()

prompt = PromptTemplate.from_template(prompt_text)
chain = RunnablePassthrough() | prompt | llm | StrOutputParser()

# === Wrap LLM as Tool ===
def generate_podcast_script(blog_text: str) -> str:
    return chain.invoke({"blog_text": blog_text})

generate_podcast_script_tool = Tool.from_function(
    name="generate_podcast_script",
    func=generate_podcast_script,
    description="Generate podcast script from blog text"
)

# === Setup Agent ===
tools = [
    scrape_blog_content,
    generate_podcast_script_tool,
    generate_podcast_audio
]

agent = initialize_agent(
    tools=tools,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# === Runner ===
def run_blog_to_podcast_agent(blog_url: str) -> str:
    result = agent.run(f"""
    Scrape the blog content from this URL: {blog_url}.
    Then generate a podcast script from it.
    Then convert that podcast script to audio.
    Return the file path of the final podcast audio.
    """)
    return result
