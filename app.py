import anthropic
from dotenv import load_dotenv
from pathlib import Path
import os
import pandas as pd
import json

# Load in the API key
load_dotenv(dotenv_path=Path(__file__).with_name(".env"))
API_KEY = str(os.getenv("MY_API"))

# Create 'Call Claude' Function. This function takes in a user's input, and returns claude's output.
def call_claude(user_message, system_prompt = None, input_model="claude-sonnet-4-5", input_max_tokens=1024):
    client = anthropic.Anthropic(api_key = API_KEY)
    if system_prompt:
        message = client.messages.create(model=input_model, max_tokens=input_max_tokens,system=system_prompt, messages = [{'role':'user','content': user_message}])
    else:
        message = client.messages.create(model=input_model, max_tokens=input_max_tokens, messages = [{'role':'user','content': user_message}])
    return message.content[0].text

def convert_topic_to_prompt(topic):
    return f"""
I am going to give you a contentious topic. Return a JSON array of exactly 5 real historical or contemporary figures who have well-documented, substantive positions on this topic.

Topic: {topic}

Rules:
- Each figure must have genuinely documented views on this topic or closely related issues
- Prioritise diversity of perspective — the 5 figures should not all agree
- Draw from relevant fields: philosophy, science, economics, politics, history, etc.

Return ONLY a JSON array with no preamble, no markdown, no backticks. Each object must have these exact fields:
- "name": full name
- "field": their primary discipline
- "era": their time period (e.g. "20th century", "Ancient Greece")
- "key_works": list of 2-3 of their most relevant works or ideas
- "known_stance": one sentence summarising their position on or most relevant to this topic
"""

def get_call1(userinput):
    raw = call_claude(convert_topic_to_prompt(userinput))
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1].strip()
        raw = raw[4:].replace("\\n","")
    data = pd.read_json(raw)
    return pd.DataFrame(data)

system_prompt = """You are staging a formal debate between two real historical figures. 

Rules:
- Voice each speaker authentically, grounded in their documented writings and philosophy
- Each speaker must argue from their actual worldview — do not invent positions they never held
- Stay in character throughout. Do not break the fourth wall or explain what you are doing
- The debate should be intellectually rigorous but accessible
- Each speaker should directly challenge the other's points, not just monologue"""

def convert_people_to_prompt(figure1, figure2, topic):
    figure1 = int(figure1)
    figure2 = int(figure2)
    return f"""Stage a debate between {df.loc[figure1, 'name']} and {df.loc[figure2, 'name']} on the following topic:

Topic: {topic}

{df.loc[figure1, 'name']} background:
- Field: {df.loc[figure1, 'field']}
- Era: {df.loc[figure1, 'era']}
- Key works: {', '.join(df.loc[figure1, 'key_works'])}
- Known stance: {df.loc[figure1, 'known_stance']}

{df.loc[figure2, 'name']} background:
- Field: {df.loc[figure2, 'field']}
- Era: {df.loc[figure2, 'era']}
- Key works: {', '.join(df.loc[figure2, 'key_works'])}
- Known stance: {df.loc[figure2, 'known_stance']}

Format the debate as follows:
- An opening statement from each figure (3-4 sentences)
- 3 rounds of back-and-forth exchange
- A closing statement from each figure (2-3 sentences)

Label each speaker clearly by their last name.

"""

def get_call2(figure1, figure2, topic):
    return call_claude(convert_people_to_prompt(figure1, figure2, topic), system_prompt=system_prompt, input_max_tokens=4096)


userinput = input("Enter a contentious topic: \n")
df = get_call1(userinput)
print(df)
figure1 = input("Please pick two people from above you would like to see a debate between ... \n Type the 1st person's index from the table above:")
figure2 = input("Type the 2nd person's index from the table above:")
debate = get_call2(figure1, figure2, userinput)
print(debate)