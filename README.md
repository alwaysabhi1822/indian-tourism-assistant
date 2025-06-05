# indian-tourism-assistant
An AI-powered chatbot that helps users discover and plan trips across India


# Incredible India Tourism Assistant


An AI-powered chatbot that helps users discover and plan trips across India. Features include:
- Destination recommendations
- Personalized travel planning
- Voice input support
- PDF itinerary generation
- Preference-based suggestions

## Features
- 🗣️ Voice-enabled queries
- 📄 PDF export for itineraries
- 🧑 User preference profiles
- 📱 Mobile-responsive design
- 🌐 Real-time information retrieval

- Install dependencies:
pip install -r requirements.txt

Set up environment:
"GROQ_API_KEY=your_groq_api_key_here" 

Run application:
uvicorn main:app --reload

Access at:
http://localhost:8000

Dependencies
Frontend: Bootstrap, FontAwesome, Animate.css
Backend: FastAPI, LangChain, Groq API
AI: Llama3-70b model



### Important Notes:

1. **Vector Store Generation**:
- Users should create their own `vectors.pkl` using the script in the README
- Replace `your_data.txt` with their custom tourism data

2. **Security**:
- The `.gitignore` excludes sensitive files (`.env`, `*.pkl`)
- Users must obtain their own [Groq API key](https://console.groq.com/)

3. **Customization Points**:
- Background image (`static/tour.webp`)
- Prompt template in `main.py`
- CSS variables in `tourismui.html`
- Safety/packing logic in `main.py`

4. **How to Run**:
```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Add Groq API key to .env
echo "GROQ_API_KEY=your_key_here" > .env

# Run application
uvicorn main:app --reload

