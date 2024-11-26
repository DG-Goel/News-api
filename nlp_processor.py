import spacy
import re

# Initialize SpaCy for NLP
nlp = spacy.load("en_core_web_sm")


# Function to extract location names from text using NLP
def extract_location(text):
    """
    Extract location names from a text input.
    Uses SpaCy to identify named entities.
    """
    doc = nlp(text)
    locations = []

    # Extract entities recognized as GPE (Geopolitical Entity)
    for ent in doc.ents:
        if ent.label_ == "GPE":
            locations.append(ent.text)

    return locations


# Function to clean and preprocess user input (optional)
def clean_input(text):
    """
    Clean the input text to remove unnecessary characters (e.g., punctuation).
    """
    # Remove punctuation and extra spaces
    text = re.sub(r'[^\w\s]', '', text)
    text = ' '.join(text.split())  # Remove extra spaces
    return text


# Function to determine if the input contains a weather request
def is_weather_request(text):
    """
    Check if the user is asking for weather-related information.
    """
    weather_keywords = ['weather', 'forecast', 'temperature', 'climate', 'humidity', 'rain', 'sunny', 'snow', 'storm']

    # Normalize the text by converting it to lowercase
    text = text.lower()

    # Check if any weather-related keyword is present in the input
    for keyword in weather_keywords:
        if keyword in text:
            return True
    return False


# Function to determine if the input contains a news request
def is_news_request(text):
    """
    Check if the user is asking for news-related information.
    """
    news_keywords = ['news', 'headlines', 'news about', 'latest news', 'breaking news', 'sports news', 'world news']

    # Normalize the text by converting it to lowercase
    text = text.lower()

    # Check if any news-related keyword is present in the input
    for keyword in news_keywords:
        if keyword in text:
            return True
    return False


# Function to extract the topic or subject from the user request
def extract_topic(text):
    """
    Extract the main topic of interest from the user's input (e.g., COVID-19, sports, etc.).
    """
    topic_keywords = [
    'covid-19', 'corona', 'virus', 'vaccine', 'infection', 'pandemic', 'quarantine', 'lockdown', 'symptoms', 'treatment', 
    'testing', 'immunity', 'variant', 'health', 'disease', 'outbreak', 'epidemic', 'contagious', 'recovery', 'spread',
    'sports', 'football', 'soccer', 'basketball', 'tennis', 'cricket', 'olympics', 'championship', 'league', 'tournament', 
    'player', 'coach', 'match', 'goal', 'score', 'fans', 'medal', 'referee', 'team', 'game', 
    'technology', 'innovation', 'artificial intelligence', 'ai', 'cybersecurity', 'software', 'app', 'internet', 'smartphone', 
    'cloud', 'gadgets', 'robotics', 'machine learning', 'automation', 'programming', 'data', 'coding', 'startup', 
    'development', 
    'politics', 'government', 'election', 'prime minister', 'president', 'parliament', 'law', 'democracy', 'constitution', 
    'congress', 'policy', 'budget', 'protest', 'campaign', 'minister', 'opposition', 'party', 'vote', 'senate', 'debate', 
    'climate', 'rain', 'storm', 'hurricane', 'cyclone', 'heatwave', 'drought', 'temperature', 'snow', 'global warming', 
    'forecast', 'sunshine', 'wind', 'clouds', 'fog', 'environment', 'pollution', 'flood', 'greenhouse', 
    'economy', 'market', 'business', 'stock', 'trade', 'investment', 'finance', 'currency', 'inflation', 'gdp', 'tax', 
    'revenue', 'profit', 'growth', 'loss', 'banking', 'export', 'import', 'entrepreneur', 'unemployment', 
    'film', 'music', 'festival', 'actor', 'actress', 'fashion', 'travel', 'food', 'movie', 'culture', 'art', 'celebrity', 
    'trends', 'awards', 'books', 'theater', 'lifestyle', 'cooking', 'showbiz', 'photography', 
    'space', 'research', 'discovery', 'nasa', 'astronomy', 'scientist', 'satellite', 'planet', 'experiment', 'galaxy', 
    'solar system', 'asteroid', 'mission', 'rocket', 'physics', 'biology', 'exploration', 'chemistry', 'telescope', 'innovation', 
    'breaking', 'update', 'headline', 'exclusive', 'viral', 'analysis', 'coverage', 'alert', 'report', 'source', 'journalist', 
    'interview', 'commentary', 'insight', 'fact', 'public', 'opinion', 'investigation', 'editorial', 'live', 
    'crime', 'justice', 'court', 'police', 'arrest', 'evidence', 'investigation', 'suspect', 'prosecution', 'trial', 
    'witness', 'fraud', 'law', 'scandal', 'victim', 'sentence', 'defense', 'verdict', 'punishment', 'lawyer'
]
    
    # Normalize text
    text = text.lower()

    # Check for topics in the input
    for keyword in topic_keywords:
        if keyword in text:
            print(f"Matched keyword for topic: {keyword}")  # Debugging line
            return keyword

    print("No matching topic found.")  # Debugging line
    return None


# Function to determine if the input contains a specific country reference for news
def is_country_news_request(text):
    """
    Check if the user is asking for news from a specific country.
    """
    country_keywords = ['from', 'about', 'in', 'on']  # Common words when referring to a country
    locations = extract_location(text)

    # Check if any country reference exists
    if locations and any(keyword in text for keyword in country_keywords):
        return locations[0]  # Return the first mentioned country for specific news
    return None


# Main function to process the user input
def process_text_command(text):
    """
    Process the user input to decide what action (weather, sports news, or general news request) should be taken and extract the location.
    Returns a dictionary with task type and location.
    """
    response = {
        "task": None,
        "location": None,
        "country_specific": False,  # Flag to indicate if the news is country-specific
        "topic_specific": False,  # Flag to indicate if the news is topic-specific
        "topic": None,  # Store the topic (like COVID-19, sports, etc.)
    }

    # Clean and preprocess the text
    text = clean_input(text)

    # Extract location from input
    locations = extract_location(text)

    if locations:
        response["location"] = locations[0]  # Taking the first location mentioned

    # Check for specific country news request
    country_news = is_country_news_request(text)
    if country_news:
        response["task"] = "news"
        response["location"] = country_news  # Set the country for news
        response["country_specific"] = True

    # Extract the topic from the text
    topic = extract_topic(text)
    if topic:
        response["task"] = "news"
        response["topic_specific"] = True
        response["topic"] = topic  # Store the topic (e.g., COVID-19, sports, etc.)

    # Determine if the user is asking about weather or general news
    elif is_weather_request(text):
        response["task"] = "weather"
    elif is_news_request(text):
        response["task"] = "news"

    return response
