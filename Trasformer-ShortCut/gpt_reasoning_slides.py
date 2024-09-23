from openai import OpenAI
import hashlib
import os
import json
from manim import *
from manim_slides import Slide

# Path to the configuration file and cache file
CONFIG_FILE = "config.json"
CACHE_FILE = "gpt_cache.json"

# Function to load API key from config.json
def load_api_key():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as file:
            config = json.load(file)
            return config.get("openai_api_key")
    raise Exception("API key not found in config.json")

# Function to hash the prompt
def hash_prompt(prompt):
    return hashlib.sha256(prompt.encode()).hexdigest()

# Function to load cache from file
def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as file:
            return json.load(file)
    return {}

# Function to save cache to file
def save_cache(cache):
    with open(CACHE_FILE, 'w') as file:
        json.dump(cache, file, indent=4)

# GPT-3 reasoning function with caching
def gpt_reasoning(prompt):
    # Load cache
    cache = load_cache()

    # Hash the prompt to use as cache key
    prompt_hash = hash_prompt(prompt)

    # Check if the response for this prompt exists in the cache
    if prompt_hash in cache:
        print("Loaded response from cache.")
        return cache[prompt_hash]

    # Load API key from config.json
    openai_api_key = load_api_key()
    client = OpenAI(
        # This is the default and can be omitted
        api_key=openai_api_key,
    )
    # If not in cache, make the API call using the new client method
    response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-3.5-turbo",
)

    # Cache the response and save it to the cache file
    cache[prompt_hash] = response['choices'][0]['message']['content'].strip()
    save_cache(cache)

    return cache[prompt_hash]

class GPT3ReasoningSlides(Slide):
    def construct(self):
        # Slide 1: Math problem
        math_title = Text("Math Problem: Solving Quadratic Equations").scale(0.6).to_edge(UP)
        self.play(Write(math_title))
        math_prompt = "Solve the quadratic equation x^2 + 5x + 6 = 0 and explain the steps."
        math_solution = gpt_reasoning(math_prompt)
        math_text = Text(math_solution).scale(0.4).next_to(math_title, DOWN)
        self.play(Write(math_text))
        self.next_slide()  # Move to next slide

        # Slide 2: Code Generation
        code_title = Text("Code Generation Example").scale(0.6).to_edge(UP)
        self.play(Write(code_title))
        code_prompt = "Write a Python function to add two numbers."
        code_generated = gpt_reasoning(code_prompt)
        code_text = Text(code_generated).scale(0.4).next_to(code_title, DOWN)
        self.play(Write(code_text))
        self.next_slide()  # Move to next slide

        # Slide 3: Logical Reasoning
        logic_title = Text("Logical Reasoning").scale(0.6).to_edge(UP)
        self.play(Write(logic_title))
        logic_prompt = "If A implies B, and A is true, what can you conclude about B?"
        logic_solution = gpt_reasoning(logic_prompt)
        logic_text = Text(logic_solution).scale(0.4).next_to(logic_title, DOWN)
        self.play(Write(logic_text))
        self.next_slide()

        # End of presentation
        self.wait(2)