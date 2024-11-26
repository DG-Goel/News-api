from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import requests
from datetime import datetime

# Constants for API URLs and Keys
SEARCH_NEWS_API_URL = "https://api.worldnewsapi.com/search-news"
NEWS_API_KEY = "6a7a8f9cef7a4f739b8a3d512a07e357"  # Replace with your valid World News API key

# Mapping of country names to ISO country codes and corresponding language codes
COUNTRY_INFO = {
    "India": {"code": "in", "language": "en"},
    "China": {"code": "cn", "language": "zh"},
    "United States": {"code": "us", "language": "en"},
    "Japan": {"code": "jp", "language": "ja"},
    "Germany": {"code": "de", "language": "de"},
    "Brazil": {"code": "br", "language": "pt"},
    "France": {"code": "fr", "language": "fr"},
    "Italy": {"code": "it", "language": "it"},
    "Spain": {"code": "es", "language": "es"},
    "United Kingdom": {"code": "gb", "language": "en"},
}

# Load PEGASUS model and tokenizer
model_name = "google/pegasus-xsum"
model = PegasusForConditionalGeneration.from_pretrained(model_name)
tokenizer = PegasusTokenizer.from_pretrained(model_name)

# Constants
MAX_TOKENS_PER_CHUNK = 1024  # Update based on the model's max token limit

def split_text_into_chunks(text, max_tokens):
    inputs = tokenizer(text, return_tensors="pt", truncation=False)
    input_length = len(inputs["input_ids"][0])  # Get the token count
    
    # If the input is too long, split into chunks
    if input_length > max_tokens:
        words = text.split()
        chunks, current_chunk, current_length = [], [], 0
        
        for word in words:
            word_length = len(tokenizer.encode(word))
            if current_length + word_length > max_tokens:
                chunks.append(" ".join(current_chunk))
                current_chunk, current_length = [word], word_length
            else:
                current_chunk.append(word)
                current_length += word_length
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
    else:
        return [text]

def generate_headlines_from_news_data(news_data):
    if not news_data or not isinstance(news_data, dict):
        return ["No valid news data provided to generate headlines."]
    
    articles = news_data.get("news", [])
    if not articles:
        return ["No articles available in the provided news data."]
    
    article_summaries = [
        f"Title: {article.get('title', 'No title available')}\nDescription: {article.get('description', 'No description available')}"
        for article in articles
    ]
    
    combined_summaries = "\n\n".join(article_summaries)
    prompt = (
        "You are a professional news assistant. Based on the following news articles, "
        "generate the best possible concise and informative headlines. Output should be in a numbered list format:\n\n"
        f"{combined_summaries}\n\n"
        "Headlines:"
    )
    
    return process_in_chunks(prompt)

def query_pegasus_summarizer(text):
    try:
        # Tokenize the input text
        inputs = tokenizer(text, truncation=True, padding="longest", return_tensors="pt")
        
        # Generate the summary (headline)
        summary_ids = model.generate(inputs["input_ids"], num_beams=4, max_length=50, early_stopping=True)
        
        # Decode the generated summary
        headline = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return headline
    except Exception as e:
        print(f"Error: {e}")
        return f"Error generating headline: {e}"

def process_in_chunks(prompt, max_tokens=MAX_TOKENS_PER_CHUNK):
    chunks = split_text_into_chunks(prompt, max_tokens)
    results = []

    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i + 1} of {len(chunks)}...")
        results.append(query_pegasus_summarizer(chunk))
    
    return results

def fetch_news_datatopic(location, topic):
    if isinstance(location, dict):
        location = location.get("city") or location.get("country")

    if not isinstance(location, str):
        print(f"Error: Invalid location format: {location}")
        return "Error: Invalid location format."

    country_info = COUNTRY_INFO.get(location)
    if not country_info:
        print(f"Error: Location '{location}' not found in the country-info map.")
        return "Error: Location not found."

    country_code = country_info["code"]
    language_code = country_info["language"]
    today_date = datetime.today().strftime('%Y-%m-%d')

    params = {
        "source-country": country_code,
        "date": today_date,
        "language": language_code,  # Ensure the language is included
        "api-key": NEWS_API_KEY,
        "text": topic
    }

    print(f"Fetching news with parameters: {params}")

    try:
        response = requests.get(SEARCH_NEWS_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        print(f"API Response: {data}")

        headlines = generate_headlines_from_news_data(data)
        return headlines

    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        return [f"Error: {e}"]
