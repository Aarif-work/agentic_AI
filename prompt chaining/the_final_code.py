import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# Load environment variables from .env (must contain OPENAI_API_KEY)
load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",  # or any other supported model
    temperature=0,
)

# --- Prompt 1: Extract Information ---
prompt_extract = ChatPromptTemplate.from_template(
    "Extract the technical specifications from the following text:\n\n{text_input}"
)

# --- Prompt 2: Transform to JSON ---
prompt_transform = ChatPromptTemplate.from_template(
    "Transform the following specifications into a JSON object "
    "with 'cpu', 'memory', and 'storage' as keys:\n\n{specifications}"
)

# --- Build the Chains using LCEL ---

# This chain: input -> prompt_extract -> llm -> plain string
extraction_chain = prompt_extract | llm | StrOutputParser()

# This full chain:
# 1. Run extraction_chain and store its output as "specifications"
# 2. Use that in prompt_transform
# 3. Call llm again
# 4. Convert to plain string
full_chain = (
    {"specifications": extraction_chain}
    | prompt_transform
    | llm
    | StrOutputParser()
)

if __name__ == "__main__":
    # --- Run the Chain ---
    input_text = (
        "The new laptop model features a 3.5 GHz octa-core processor, "
        "16GB of RAM, and a 1TB NVMe SSD."
    )

    # Execute the chain with the input text dictionary.
    final_result = full_chain.invoke({"text_input": input_text})

    print("\n--- Final JSON Output ---")
    print(final_result)