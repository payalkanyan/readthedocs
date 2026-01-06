from langchain_text_splitters import RecursiveCharacterTextSplitter

def preprocess_text(all_text: str):
    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000, 
            chunk_overlap = 200, 
            length_function = len,
            separators=['\n', '\n\n', ' ', '']
        )
        
    chunks = text_splitter.split_text(text = all_text)

    return chunks

