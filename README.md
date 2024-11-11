## About

This tool transcribes audio to text using OpenAI's [Speech to text API](https://platform.openai.com/docs/guides/speech-to-text), and post process it using [Text generation API](https://platform.openai.com/docs/guides/text-generation).

## Getting started

## Pre-requisitions

Before you begin, ensure you have met the following requirements:

- You have `ffmpeg` installed. Please refer to [Getting ffmpeg set up](https://github.com/jiaaro/pydub#getting-ffmpeg-set-up)
- You have a valid OpenAI API key and configurated.
- You have Python 3.9 or higher installed on your machine.

### Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:actuallyyun/JoyScribe.git
   ```
2. Navigate to the project directory:
   ```bash
   cd JoyScribe
   ```

3. Install the required dependencies. You can do this by running:
  ```bash
  pip install -r requirements.txt
  ```

### How to use 
1. Open a terminal and navigate to the project directory.
2. Run the script with the following command:
   ```bash
   python transcribe.py --file <path_to_audio_file> --output <output_directory>
   ```
   Replace `<path_to_audio_file>` with the path to your audio file and `<output_directory>` with the directory where you want to save the output files.

3. Wait for the the program to finish. You can follow the terminal to see the progress.

![terminal progress](./images/Screenshot%202024-11-11%20at%2015.40.18.png)


**To customize the prompt in the `post_processing.py` file, you can modify the `system_prompt` variable.**


## How I built it

1. Test it with short audio 

> By default, the Whisper API only supports files that are less than 25 MB. 

This is a limitation I have to address since my audio files are bigger than 25 MB.

But first, I want to make sure my setup with OpenAI works. 

So I tested it with a shorter audio, run the script, waited for a few seconds, and woala, it worked.

2. Research solutions for longer audio inputs

[OpenAI's documentation](https://platform.openai.com/docs/guides/speech-to-text) recommened the to use [the PyDub open source Python package to split the audio](https://github.com/jiaaro/pydub)

But this packages has some dependencies, and one of which is `ffmpeg`. The [offical ffmpeg website](https://ffmpeg.org/download.html#build-mac) is a bit confusing and only provides download option.

I use Mac OS and perfer install packages with `brew`. And indeed, `brew` has this package. 

3. The logic is straightforward: cut the audio into smaller chunks, save it to a directory and pass the segement one by one to `whisper`.



## Optimizations

Up until this point,it does the job transcribing it. However, the response is not easy to read. It does not include puncutations and does not have formatting. 

Using `gpt` to post process the transcript is a common practice. 

To simplify things, I decided to use one assistant for the job. It does the following:

- Format the text
- Convert traditional Chinese characters to simplified Chinese
- Format English with Chinese translations included in parenthese
- Extract subheading every 4 paragraphs 


## Future improvements 

1. Keep fine tuning the assistant to be more useful. 

2. Clean the audio before segementing. For example, trim leading silence in audio, this increases Wisper's transcribing performance. 

## Got suggestions? 

For any inquiries or feedback, please reach out to:

- **Name**: Yun Ji
- **Email**: [this.jiyun@gmail.com](mailto:this.jiyun@gmail.com)
- **LinkedIn**: [your-linkedin-profile](https://www.linkedin.com/in/yun-ji)

Feel free to connect with me!



