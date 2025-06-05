from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
import os
from pydantic import BaseModel
from dotenv import load_dotenv
import pickle

load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Load models and vector store
try:
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    with open("vectors.pkl", "rb") as f:
        vectors = pickle.load(f)
    if not hasattr(vectors, 'similarity_search'):
        raise ValueError("Invalid vector store format")
except Exception as e:
    raise RuntimeError(f"Error loading vector store: {e}")

llm = ChatGroq(groq_api_key=os.getenv('GROQ_API_KEY'), model_name="llama3-70b-8192")

# Proper prompt template with all required variables
prompt = ChatPromptTemplate.from_template(
    """
    You are an expert Indian tourism assistant. Your responsibilities include:

    1. **Top Tourist Destinations**: Recommend the best tourist destinations within any state or city in India. Provide detailed information on:
       - History: The historical significance of each location.
       - Cultural Significance: The cultural importance and unique features.
       - Must-See Attractions: Key attractions that visitors should not miss.

    2. **Restaurant Recommendations**: Offer detailed restaurant suggestions near the recommended destinations, categorized by:
       - Dietary Preferences: {dietary_preference}
       - Must-Try Cuisine: Specific dishes that are renowned or unique to that location.

    3. **Best Time to Visit**: Advise on the optimal time of the year to visit each location. Consider factors such as:
       - Weather: Ideal weather conditions for travel.
       - Local Festivals: Significant festivals or events.
       - Tourist Footfall: Peak and off-peak tourist seasons.

    4. **Complete Travel Schedules**: For users wanting to tour an entire state, provide a comprehensive itinerary including:
       - Significant Attractions: Major sites and experiences.
       - Cultural Experiences: Opportunities to engage with local culture.
       - Local Specialties: Unique local foods and activities.

    5. **Safety Alerts**: {safety_alerts}

    6. **Packing Recommendations**: {packing_recommendations}

    **Instructions for responding:**
    - If the user greets (e.g., "hi", "hello", "hey"), greet them back politely and do not show any travel plan unless they ask for it.
    - If the user only asks about a place (e.g., "Tell me about Jaipur"), provide only relevant information like history, culture, and attractions—**do not** include restaurants, itineraries, or cuisine unless explicitly asked.
    - Format your response clearly:
        - Use **bold** for section headers
        - Separate each day's activities (if itinerary) into distinct sections
        - Use bullet points for clarity
        - Keep paragraphs short (2-3 sentences max)
        - Add emojis to enhance friendliness when appropriate

    Current conversation history:
    {history}

    User preferences:
    - Group size: {num_members}
    - Children: {children}
    - Adults: {adults}
    - Seniors: {seniors}
    - Dietary: {dietary_preference}

    <context>
    {context}
    </context>
    
    Question: {input}
    
    Answer:
    """
)


# Create chains
doc_chain = create_stuff_documents_chain(llm, prompt)
retriever = vectors.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, doc_chain)

class ChatRequest(BaseModel):
    message: str
    preferences: dict
    history: str = ""

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("tourismui.html", {"request": request})

@app.post("/chat")
async def chat_endpoint(chat_request: ChatRequest):
    try:
        prefs = chat_request.preferences
        response = retrieval_chain.invoke({
            "input": chat_request.message,
            "history": chat_request.history,
            "num_members": prefs.get("num_members", 1),
            "children": prefs.get("children", 0),
            "adults": prefs.get("adults", 1),
            "seniors": prefs.get("seniors", 0),
            "dietary_preference": prefs.get("dietary", "Not specified"),
            "safety_alerts": generate_safety_alerts(prefs),
            "packing_recommendations": generate_packing_recommendations(chat_request.message),
            "context": ""
        })
        return {"response": response["answer"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generate_safety_alerts(prefs):
    if int(prefs.get("children", 0)) > 0 or int(prefs.get("seniors", 0)) > 0:
        return "Safety Alert: For groups with children or seniors, exercise caution at mountainous or ocean destinations"
    return "No specific safety alerts"

def generate_packing_recommendations(query):
    if "beach" in query.lower():
        return "Packing: swimwear, sunscreen, sunglasses, flip-flops"
    elif any(word in query.lower() for word in ["mountain", "hill", "cold"]):
        return "Packing: warm jackets, thermal wear, snow boots, gloves, scarves"
    return "General packing: comfortable clothes, medications, travel documents"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)