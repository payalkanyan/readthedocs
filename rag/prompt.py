from langchain_core.prompts  import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder

def get_prompt():
    prompt_template = """Answer the question as precise as possible using the provided context. If the answer is
                    not contained in the context, say "answer not available in context" \n\n
                    Context: \n {context}?\n
                    Question: \n {question} \n
                    Answer:"""

    prompt = PromptTemplate.from_template(template=prompt_template)

    return prompt