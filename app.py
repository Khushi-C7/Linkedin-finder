import streamlit as st
import requests

# Set your API keys here
groq_api_key = 
serpapi_key = 

def generate_search_query(name):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [{
            "role": "user",
            "content": f"Generate a Google search query to find the LinkedIn profile of a person named '{name}'. Only return the query."
        }],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    
    return data['choices'][0]['message']['content'].strip().replace('"', '')

def search_linkedin_profiles(query):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": query,
        "api_key": serpapi_key
    }
    response = requests.get(url, params=params)
    results = response.json()
    links = []

    if "organic_results" in results:
        for result in results["organic_results"]:
            link = result.get("link", "")
            if "linkedin.com/in" in link.lower():
                links.append(link)
    return links

# Streamlit UI
st.title("🔍 LinkedIn Profile Finder")
st.write("Enter a person's name to find their LinkedIn profile using LLaMA-3 + SerpAPI.")

name = st.text_input("👤 Enter full name")

if st.button("🔎 Search"):
    if name:
        with st.spinner("🧠 Generating search query..."):
            query = generate_search_query(name)

        st.markdown(f"**Generated Query:** `{query}`")

        with st.spinner("🌐 Searching Google for LinkedIn profiles..."):
            profiles = search_linkedin_profiles(query)

        if profiles:
            st.success("✅ Found the following profiles:")
            for url in profiles:
                st.markdown(f"- [LinkedIn Profile]({url})")
        else:
            st.warning("😕 No profiles found.")
    else:
        st.error("Please enter a name.")
