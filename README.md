# Raspberry Pi Voice Assistant using OpenAI API

This repository contains the code for a Raspberry Pi-based voice assistant that leverages the OpenAI API to answer user queries. The voice assistant activates each time the user presses a button, allowing them to ask questions and receive responses based on the inputs provided.

## Features

- **Voice Activation**: The assistant is triggered by a physical button press.
- **OpenAI Integration**: Uses the OpenAI API to process and generate responses.
- **Easy Setup**: Simple script with minimal dependencies.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following:

- A Raspberry Pi with a working microphone and speaker.
- Python 3 installed on your Raspberry Pi.
- An OpenAI API key.

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/manishacharya60/raspberryPi_voice_assistant.git
    ```

2. **Create a `.env` file**:
    Create a `.env` file in the root directory of the project to store your OpenAI API key.
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```

3. **Install the required Python packages**:
    Install the necessary dependencies by running:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the script**:
    Once everything is set up, you can run the voice assistant script:
    ```bash
    python script.py
    ```

### How It Works

- The script continuously listens for a button press. Once the button is pressed, the assistant will prompt the user to ask a question.
- The question is then sent to the OpenAI API, and the response is read aloud to the user.

## Customization

You can customize the functionality by modifying `script.py` as needed. Make sure to keep your OpenAI API key secure by storing it in the `.env` file and not hardcoding it into the script.

## Troubleshooting

- **No Response**: Ensure your microphone and speaker are properly connected and configured.
- **Invalid API Key**: Double-check that your API key is correctly set in the `.env` file.
- **Dependencies Issue**: Make sure all dependencies in `requirements.txt` are installed.

## Contact

For any questions or suggestions, feel free to open an issue.
