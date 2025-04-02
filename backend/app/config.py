import os
from dotenv import load_dotenv


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
API_TITLE = "AuditAI Chatbot API"
ALLOWED_ORIGINS = ["http://localhost:5173"]
UPLOAD_DIR = "backend/app/contracts"