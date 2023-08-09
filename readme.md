
# GPTTWEETER: Thread Generator 🐦

GPTTWEETER is a powerful tool designed to automatically generate engaging and viral Twitter threads based on a given topic. Powered by OpenAI's advanced GPT model, this app fetches relevant articles, summarizes them, and constructs a compelling Twitter thread ready to captivate your audience.

## Features:

1. **Relevant Article Search:** Uses the SERP API to fetch the most relevant articles based on the user's query.
2. **Advanced Article Selection:** Utilizes OpenAI's GPT model to select the top 5 most pertinent articles.
3. **Comprehensive Summarization:** Extracts and summarizes the content of chosen articles.
4. **Thread Generation:** Constructs a Twitter thread using the summarized content, ensuring it's engaging and viral.

## How to Use:

1. Run the app.
2. Input your desired topic in the Streamlit interface.
3. Wait for the magic to happen! The app will fetch articles, choose the best ones, summarize them, and then construct a Twitter thread.
4. Review and post your new viral thread!

## Setup and Installation:

### Prerequisites:

- Python 3.9 or newer
- Streamlit, OpenAI, langchain, dotenv, requests, and json libraries installed.

### Steps:

1. Clone the repository to your local machine.
2. Navigate to the root directory of the project.
3. Install the required libraries using pip:

    ```bash
    pip install streamlit openai langchain python-dotenv requests
    ```

4. Create a `.env` file in the root directory and add your SERP API key and OpenAI API key:

    ```env
    SERPER_API_KEY=your_serper_api_key
    OPENAI_API_KEY=your_openai_api_key
    ```

5. Run the app using:

    ```bash
    streamlit run app.py
    ```

6. Navigate to the URL provided in the terminal to access the Streamlit interface.

## Contributions:

Feel free to fork this project, submit PRs, and contribute to enhancing its capabilities.

---
