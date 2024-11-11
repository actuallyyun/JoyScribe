from openai import OpenAI
import os

client = OpenAI()

def edit_assistant(transcript):
    
    system_prompt = """You are an intelligent assistant specializing in journalism. 
    Your task is to process interview transcripts, ensuring that it is formatted correctly, 
    all traditional Chinese characters are converted to simplified Chinese, and all English words
    are in the correct format. 
    You do not translate English words to Chinese, instead, you add the translation in parenthese. For example,
    'bachelor study' should be transformed to 'bachelor study(本科学习)',
    'industrial engineering and management' should be transformed to 'Industrial Engineering and Management(工业工程和管理)'
    You add punctuations to the text, such as periods, commas, capialization, question marks.
    You add paragraph break after each question.
    For every 4 paragraphs, you extract a sub heading. For example,"对未来职业发展的规划". 
    Use only the context provided. If there is no context provided say, 'No context provided'\n"""
    
    response=client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": transcript
                }
            ]
        )

    return response

# Function to split the transcript into manageable chunks
def split_transcript(transcript, max_tokens):
    words = transcript.split()
    chunks = []
    current_chunk = []

    for word in words:
        current_chunk.append(word)
        if len(' '.join(current_chunk)) > max_tokens:  # Check if the chunk exceeds the limit
            chunks.append(' '.join(current_chunk[:-1]))  # Add the current chunk to the list
            current_chunk = [word]  # Start a new chunk with the last word

    if current_chunk:  # Add any remaining words as the last chunk
        chunks.append(' '.join(current_chunk))

    return chunks

# Define the maximum number of tokens for the model 


def read_transcript_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def post_processing(output_path,transcript_file_path):
     
     # Read the transcript from a specified file
    transcript = read_transcript_from_file(transcript_file_path)

    max_tokens = 6000 

    # break the transcript down to consumable chunks
    transcript_chunks = split_transcript(transcript, max_tokens)

    # Use transcript editing assistant
    edited_transcripts=[]

    print(f"{len(transcript_chunks)} chunks in total")

    for index, chunk in enumerate(transcript_chunks):
        
        print(f"Chunk {index+1}: using assistant...")

        response=edit_assistant(chunk)
        edited_transcript=response.choices[0].message.content
        print(edited_transcript)
        edited_transcripts.append(edited_transcript)


    full_edited_transcript=' '.join(edited_transcripts)

    output_path=os.path.join(output_path, 'edited_full_transcript') 
    
    # save the edited transcript 
    with open(output_path, 'w', encoding='utf-8') as file:
            file.write(full_edited_transcript)


