from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain.agents import Tool
from langchain_core.tools import tool
from tools import scrape_blog_content, generate_podcast_audio
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(dotenv_path="d:/PROJECTS/AI AGENT/ai-blogs-to-podcast/.env")
# === Nebius Setup ===
nebius_api_key = os.getenv("NEBIUS_API_KEY")
nebius_api_base = "https://api.studio.nebius.com/v1/"

if not nebius_api_key:
    raise ValueError("NEBIUS_API_KEY not found in environment variables.")

# Create OpenAI client for direct API calls
client = OpenAI(api_key=nebius_api_key, base_url=nebius_api_base)

# Use Qwen model via OpenAI compatible API with LangChain
llm = ChatOpenAI(
    model_name="Qwen/Qwen3-235B-A22B",
    temperature=0.6,
    top_p=0.95,
    openai_api_key=nebius_api_key,
    openai_api_base=nebius_api_base,
)

# === Prompt Setup ===
with open("prompts/podcast_prompt.txt", encoding="utf-8") as f:
    prompt_text = f.read()

prompt = PromptTemplate.from_template(prompt_text)


# Use RunnableLambda for custom input mapping
def input_mapper(inputs: dict) -> dict:
    return {"blog_text": inputs["blog_text"]}


chain = RunnableLambda(input_mapper) | prompt | llm | StrOutputParser()


# === Wrap LLM as Tool ===
@tool
def generate_podcast_script(blog_text: str) -> str:
    """Generate podcast script using LangChain."""
    return chain.invoke({"blog_text": blog_text})


def generate_podcast_script_direct(blog_text: str) -> str:
    """Generate podcast script using direct OpenAI client."""
    response = client.chat.completions.create(
        model="Qwen/Qwen3-235B-A22B",
        temperature=0.6,
        top_p=0.95,
        messages=[
            {
                "role": "system",
                "content": prompt_text.replace("{blog_text}", blog_text),
            },
        ],
    )
    return response.choices[0].message.content


generate_podcast_script_tool = Tool.from_function(
    name="generate_podcast_script",
    func=generate_podcast_script,
    description="Generate podcast script from blog text",
)


# === Runner ===
def run_blog_to_podcast_agent(blog_url: str) -> str:
    """
    Convert a blog post to a podcast audio file.

    Args:
        blog_url: URL of the blog post to convert

    Returns:
        Path to the generated audio file
    """
    blog_content = scrape_blog_content.run(blog_url)
    podcast_script = generate_podcast_script_tool.run(blog_content)
    audio_path = generate_podcast_audio.run(podcast_script)
    return audio_path


__all__ = [
    "run_blog_to_podcast_agent",
    "generate_podcast_script",
    "generate_podcast_script_direct",
]
