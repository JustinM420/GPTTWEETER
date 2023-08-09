import os
from dotenv import find_dotenv, load_dotenv
import requests
import json
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
import openai
import streamlit as st

load_dotenv(find_dotenv())
SERPAPI_API_KEY = os.getenv("SERPER_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

# 1. Serp Request to get list of relevant articles


def search(query):
    url = "https://google.serper.dev/search"

    payload = json.dumps({
        "q": query
    })
    headers = {
        'X-API-KEY': SERPAPI_API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_data = response.json()

    print("search results: ", response_data)
    return response_data


# 2. llm to choose the best articles, and return urls

def find_best_article_urls(response_data, query):
    #turn json object into string
    response_str = json.dumps(response_data)

    #create llm to choose best articles
    llm = OpenAI(model_name="gpt-3.5-turbo-16k", temperature=.7)
    template = """
    You area world class journalist & researcher, you are extremly good at finding most relevant articles to a certain topic;
    {response_str}
    Above is the list of search results for the query {query}.
    Please choose the best 5 articles from the list, return ONLY an array of the urls, do not include anything else; return ONLY an array of the urls, do not include anything else.
    """

    prompt_template = PromptTemplate(
        input_variables=["response_str", "query"], template=template)
    
    article_picker_chain = LLMChain(
        llm=llm, prompt=prompt_template, verbose=True)
    
    urls = article_picker_chain.predict(response_str=response_str, query=query)

    #convert string to list
    url_list = json.loads(urls)
    print(url_list)
    return url_list

# 3. get content for each article from urls and make summaries

def get_content_from_urls(urls):
    #use unstructuredURLLoader
    loader = UnstructuredURLLoader(urls=urls)
    data = loader.load()

    return data

def summarize(data, query):
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=3000, chunk_overlap=200, length_function=len)
    text = text_splitter.split_documents(data)

    llm = OpenAI(model_name="gpt-3.5-turbo-16k", temperature=.7)
    template = """
    {text}
    You are a world class journalist, and you will try to summarise the text above in order to create a twitter thread about {query}
    Please follow all of the following rules:
    1/ Make sure the content is engaging, informative with good data
    2/ Make sure the content is not too long, it should not be more than 4-7 tweets each with a max length of 500 characters. 
    3/ The content should address the {query} topic very well
    4/ The content needs to be viral, and get at least 1000 likes
    5/ The content needs to be written in a way that is easy to read and understand, you can use bold and italic text formatting to improve readability
    6/ The content needs to give audience actionable advice & insights
    7/ At the end add one additional thread with a Call to Action to follow   

    Summary:   
    """

    prompt_template = PromptTemplate(input_variables=["text", "query"], template=template)

    summarise_chain = LLMChain(llm=llm, prompt=prompt_template, verbose=True)

    summaries = []

    for chunk in enumerate(text):
        summary = summarise_chain.predict(text=chunk, query=query)
        summaries.append(summary)

    print(summaries)
    return summaries
    


# 4. Turn summarization into twitter thread

def generate_thread(summaries, query):
    summaries_str = str(summaries)
    
    llm = OpenAI(model_name="gpt-3.5-turbo-16k", temperature=.7)
    template = """
    {summaries_str}

    You are a world class journalist and twitter influencer, text above in order to create a twitter thread about {query}
    Please wirte a viral twitter thread about {query} using the text above, follow all rules below:
    1/ Make sure the content is engaging, informative with good data
    2/ Make sure the content is not too long, it should not be more than 4-7 tweets each with a max length of 500 characters. 
    3/ The content should address the {query} topic very well
    4/ The content needs to be viral, and get at least 1000 likes
    5/ The content needs to be written in a way that is easy to read and understand, you can use bold and italic text formatting to improve readability
    6/ The content needs to give audience actionable advice & insights
    7/ At the end add one additional thread with a Call to Action to follow   

    TWITTER THREAD:   
    """

    prompt_template = PromptTemplate(input_variables=["summaries_str", "query"], template=template)
    twitter_thread_chain = LLMChain(llm=llm, prompt=prompt_template, verbose=True)

    twitter_thread = twitter_thread_chain.predict(summaries_str=summaries_str, query=query)

    return twitter_thread


# 5. Create GUI with streamlit

def main():
    st.set_page_config(page_title="GPTTWEETER", page_icon=":bird:", layout="wide")

    st.header("GPTTWEETER: Thread Generator :bird: :thread:")
    query = st.text_input("Topic of twitter thread")

    if query:
        print(query)
        st.write("Generating twitter thread for: ", query)

        search_results = search(query)
        urls = find_best_article_urls(search_results, query)
        data = get_content_from_urls(urls)
        summaries = summarize(data, query)
        thread = generate_thread(summaries, query)

        with st.expander("search results"):
            st.info(search_results)
        with st.expander("best urls"):
            st.info(urls)
        with st.expander("data"):
            st.info(data)
        with st.expander("summaries"):
            st.info(summaries)
        with st.expander("thread"):
            st.info(thread)

if __name__ == '__main__':
    main()