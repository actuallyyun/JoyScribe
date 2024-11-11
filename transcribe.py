from openai import OpenAI
from pydub import AudioSegment
import os 
import shutil
from post_processing import post_processing
import argparse  # Import argparse for command line arguments

client = OpenAI()

# functions to trim the leading silence at the beginning of the audio file

def transcribe_audio(audio_file,output_dir):
    audio_path=os.path.join(output_dir,audio_file)
    print(f"Start transcribing ${audio_path}")
    with open(audio_path, 'rb') as audio_data:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", file=audio_data)
        
        return transcription.text


# use PyDub to cut audio in smaller chunks
def segment_audio(audio_file,output_dir,duration):
    print("Start segmenting audio...")
    
    start_time=0
    i=0

    if os.path.isdir(output_dir): 
        print("Directory already exists. Deleting...")
        shutil.rmtree(output_dir)  # Delete output directory and all its contents

    if not os.path.isdir(output_dir):  # Create the output directory if it does not exist
        print("Creating new directory...")
        os.makedirs(output_dir)

    while start_time<len(audio_file):
        print(f"Segementing audio {i+1}")
        segment=audio_file[start_time:start_time+duration]
        segment.export(os.path.join(output_dir, f"segemented_{i:02d}.mp3"), format="mp3")
        start_time+=duration
        i+=1

    audio_files=sorted((f for f in os.listdir(output_dir) if f.endswith(".mp3")),
        key=lambda f: int(''.join(filter(str.isdigit, f))))
    print("Finished segmenting audio.")
    return audio_files

# Add this function to parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Transcribe audio files.")
    parser.add_argument('--file', required=True, help='Path to the audio file to transcribe')
    parser.add_argument('--output', required=True, help='Directory to save the output files')
    return parser.parse_args()

if __name__ == "__main__":  # Add this block to run the script
    args = parse_args()  # Parse command line arguments
    interview_audio = args.file  # Use the file from command line args
    output_dir = args.output  # Use the output directory from command line args

    # Load the original file
    interview = AudioSegment.from_file(interview_audio, "mp4")

    # Generate output directory name based on the input file name
    base_name = os.path.splitext(os.path.basename(interview_audio))[0]
    print('The base name is: '+base_name)
    output_dir = os.path.join(output_dir, base_name)  # Create a subdirectory based on the file name
    print(f"The output dir is ${output_dir}")

    ten_minutes = 10 * 60 * 1000  # Define duration for each segment

    interview_files=segment_audio(interview,output_dir,ten_minutes)

    transcriptions = [transcribe_audio(file,output_dir) for file in interview_files]
    # Concatenate the transcriptions
    full_transcript = ' '.join(transcriptions)


    # Output the full_transcript into a file in the output_dir
    full_transcript_file_path = os.path.join(output_dir, 'full_transcript.txt')  # Specify the output file name
    with open(full_transcript_file_path, 'w', encoding='utf-8') as f:  # Open the file in write mode
        f.write(full_transcript)  # Write the transcript to the file

    # User assistant to edit transcript
    post_processing(output_dir,full_transcript_file_path)
