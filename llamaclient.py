from groq import Groq

# Initialize Llama API client
client = Groq(api_key="YOUR_API_KEY")  # Replace with your actual API key

def query_llama(prompt, model="llama-3.1-70b-versatile", temperature=0.3, max_tokens=500):
    """
    Sends a prompt to the Llama API and returns the response.
    Args:
        prompt (str): The prompt to send to the Llama model.
        model (str): Llama model version to use.
        temperature (float): Sampling temperature for response creativity.
        max_tokens (int): Max number of tokens in the response.
    Returns:
        list: A list of parsed headlines or the raw response in case of an error.
    """
    try:
        # Make the API call
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a professional news assistant specialized in creating headlines."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1,
            stream=False,
            stop=["\n\n"]
        )
        # Parse the response
        response = completion.choices[0].message.content.strip()
        return [line.strip() for line in response.split("\n") if line.strip()]
    except Exception as e:
        print(f"Llama API Error: {e}")
        return [f"Error communicating with Llama: {e}"]

def generate_headlines_from_news_data(news_data):
    """
    Processes raw news data and generates the best headlines using the Llama API.
    Args:
        news_data (dict): The raw news data, typically containing a list of articles.
    Returns:
        list: A list of generated headlines.
    """
    if not news_data or not isinstance(news_data, dict):
        return ["No valid news data provided to generate headlines."]

    # Extract key article information
    articles = news_data.get("news", [])
    if not articles:
        return ["No articles available in the provided news data."]

    # Prepare a summarized string of news articles
    article_summaries = []
    for article in articles:
        title = article.get("title", "No title available")
        description = article.get("description", "No description available")
        article_summaries.append(f"Title: {title}\nDescription: {description}")

    # Combine all summaries into a single string
    combined_summaries = "\n\n".join(article_summaries)

    # Build a prompt for the Llama API
    prompt = (
        "You are a professional news assistant. Based on the following news articles, "
        "generate the best possible concise and informative headlines. Output should be in a numbered list format:\n\n"
        f"{combined_summaries}\n\n"
        "Headlines:"
    )

    # Send the prompt to Llama and get the response
    return query_llama(prompt)
