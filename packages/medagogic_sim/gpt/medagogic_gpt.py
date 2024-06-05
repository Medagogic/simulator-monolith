from typing import List, TypedDict
from dotenv import load_dotenv
from openai.types.chat import ChatCompletion

load_dotenv(".env")

USE_CACHE = False

if USE_CACHE:
    from packages.medagogic_sim.gpt.cached_openai import openai, configure_cached_openai
    configure_cached_openai()
    openai_client = openai
else:
    from openai import AsyncOpenAI
    openai_client = AsyncOpenAI()


MODEL_GPT4 = "gpt-4o"
MODEL_GPT35 = "gpt-3.5-turbo"
TEMPERATURE = 0    # 0 = predictable, 2 = chaotic

GPTMessage = TypedDict("GPTMessage", {"role": str, "content": str})

def SystemMessage(content: str) -> GPTMessage:
    return {"role": "system", "content": content}

def UserMessage(content: str) -> GPTMessage:
    return {"role": "user", "content": content}


async def gpt(messages: List[GPTMessage], model=MODEL_GPT4, max_tokens=500, temperature=TEMPERATURE, cache_skip=False) -> str:
    kwargs = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "n": 1,
        "temperature": temperature
    }

    if USE_CACHE:
        kwargs["cache_skip"] = cache_skip

    openai_response: ChatCompletion = await openai_client.chat.completions.create(**kwargs)

    return openai_response.choices[0].message.content


async def gpt_streamed_lines(messages: List[GPTMessage], model=MODEL_GPT4, max_tokens=500, temperature=TEMPERATURE):
    response_stream = await openai_client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                n=1,
                temperature=temperature,
                stream=True
            )

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