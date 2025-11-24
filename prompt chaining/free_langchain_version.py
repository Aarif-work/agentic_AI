import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import AIMessage

# Mock function that simulates LLM responses
def mock_llm(messages):
    content = messages.messages[0].content
    
    if "Extract the technical specifications" in content:
        return AIMessage(content="CPU: 3.5 GHz octa-core processor\nMemory: 16GB RAM\nStorage: 1TB NVMe SSD")
    
    if "Transform the following specifications" in content:
        return AIMessage(content='{"cpu": "3.5 GHz octa-core processor", "memory": "16GB", "storage": "1TB NVMe SSD"}')
    
    return AIMessage(content="No response")

# Convert function to runnable
llm = RunnableLambda(mock_llm)

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
extraction_chain = prompt_extract | llm | StrOutputParser()
full_chain = (
    {"specifications": extraction_chain}
    | prompt_transform
    | llm
    | StrOutputParser()
)

if __name__ == "__main__":
    input_text = (
        "The new laptop model features a 3.5 GHz octa-core processor, "
        "16GB of RAM, and a 1TB NVMe SSD."
    )

    final_result = full_chain.invoke({"text_input": input_text})

    print("\n--- Final JSON Output ---")
    print(final_result)