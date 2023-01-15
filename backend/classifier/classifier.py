import os
import sys
import logging
import json
import string
from typing import Iterator
import math
import itertools

import openai

TOKEN_SIZE = 4
MAX_TOKENS = 4000
EXPECTED_INPUT_OUTPUT_RATIO = .7
PROMPT_TEMPLATE = string.Template("""
$user_info

Given is a list of bank statements and a list of the corresponding categories,
the categories are a list of lists as each statement has multiple categories.
statements:
$statements
categories:
""")

logging_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging_formatter)
logger = logging.getLogger(__name__)
logger.addHandler(handler)


def split_list_by_indices(lst: list[any], indices: list[int]):
    indices.sort()
    return [lst[i:j] for i, j in zip([None, *indices], [*indices, None])]


def calculate_tokens(text: str) -> int:
    return len(text) / TOKEN_SIZE


def create_prompts(statements: list[list[str]], user_info="", n_splits=1) -> Iterator[str]:
    split_step = len(statements) // n_splits
    split_ids = list(range(split_step, len(statements), split_step))
    for sub_statements in split_list_by_indices(statements, split_ids):
        yield PROMPT_TEMPLATE.substitute(statements=sub_statements, 
            user_info=user_info)

def execute_prompt(prompt: str) -> str:
    max_tokens = math.floor(MAX_TOKENS * (1-EXPECTED_INPUT_OUTPUT_RATIO))
    logger.debug(f"Sending request with {prompt=}")
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=max_tokens,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    logger.debug(f"{response=}")
    return response.get("choices")[0]["text"]


def classify_statements(statements, user_info="") -> list[str]:
    """
    """
    user_info_size = calculate_tokens(user_info)
    statements_size = calculate_tokens(str(statements))
    prompt_size = calculate_tokens(PROMPT_TEMPLATE.template)
    expected_size = user_info_size + statements_size + prompt_size
    MAX_SIZE =  math.floor(MAX_TOKENS * EXPECTED_INPUT_OUTPUT_RATIO)
    needed_prompts =math.ceil(expected_size / MAX_SIZE)
    prompts = create_prompts(statements, user_info, needed_prompts)
    results = []
    for prompt in prompts:
        results.append(execute_prompt(prompt))
    parsed_results = (eval(result) for result in results)
    flattened_results = list(itertools.chain.from_iterable(parsed_results))
    return flattened_results

def get_models():
    models_response = openai.Model.list()
    for model in models_response["data"]:
        yield model["id"]


def main():
    for model in get_models:
        logger.info(model["id"])

if __name__ == "__main__":
    main()
