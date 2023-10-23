from typing import List, TypedDict
from tenacity import retry, wait_fixed
from dotenv import load_dotenv
from packages.medagogic_sim.gpt.cached_openai import openai, configure_cached_openai
import os, json

load_dotenv()
configure_cached_openai()

MODEL_GPT4 = "gpt-4"
MODEL_GPT35 = "gpt-3.5-turbo"
TEMPERATURE = 0.1    # 0 = predictable, 2 = chaotic
TOP_P = 1

GPTMessage = TypedDict("GPTMessage", {"role": str, "content": str})

def SystemMessage(content: str) -> GPTMessage:
    return {"role": "system", "content": content}

def UserMessage(content: str) -> GPTMessage:
    return {"role": "user", "content": content}


async def gpt(messages: List[GPTMessage], model=MODEL_GPT4, max_tokens=500, temperature=TEMPERATURE, top_p=TOP_P, show_usage=False, presence_penalty=0, frequency_penalty=0) -> str:
    kwargs = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "n": 1,
        "top_p": top_p,
        "stop": None,
        "temperature": temperature,
        "presence_penalty": presence_penalty,
        "frequency_penalty": frequency_penalty,
    }
    response = await openai.ChatCompletion.acreate(**kwargs)

    return response["choices"][0]["message"]["content"]


@retry(wait=wait_fixed(1))
async def gpt_streamed_lines(messages: List[GPTMessage], model=MODEL_GPT4, max_tokens=500, temperature=TEMPERATURE, top_p=TOP_P, show_usage=False, presence_penalty=0, frequency_penalty=0):
    try:
        response_stream = await openai.ChatCompletion.acreate(
                    model=model,
                    messages=messages,
                    max_tokens=max_tokens,
                    n=1,
                    top_p=top_p,
                    stop=None,
                    temperature=temperature,
                    presence_penalty=presence_penalty,
                    frequency_penalty=frequency_penalty,
                    stream=True
                )
    except Exception as e:
        with open("gpt_error.json", "w") as f:
            json.dump(messages, f, indent=4)
        print(f"GPT error: {e}")
        print(f"Input context dumped to gpt_error.json")
        raise e

    current_line = ""
    async for response in response_stream:
        delta = response["choices"][0]["delta"]
        if "finish_reason" in delta:
            finish_reason = delta["finish_reason"]
            if finish_reason:
                break
        if "content" in delta:
            content: str = delta["content"]
            if "\n" in content:
                a, b = content.split("\n", 1)
                current_line += a.strip()
                yield current_line
                current_line = b.strip()
            else:
                current_line += delta["content"]
    yield current_line