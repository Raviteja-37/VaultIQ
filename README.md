# VaultIQ — AI-Powered Banking Knowledge Chatbot

Jatayu Season 5 | Use Case 2

## What it does
A secure, role-aware RAG-powered knowledge chatbot for banking operations teams.

## Features
- 6-role JWT authentication (Customer → Executive)
- RAG pipeline with source citations and confidence scoring
- Role-based access control enforced at vector DB layer
- Security alert system — breach attempts notify managers silently
- Auto ticket raising for unresolved customer queries
- Full audit trail — every query logged with source, role, timestamp

## Tech Stack
- **Backend:** FastAPI, SQLAlchemy, ChromaDB, LangChain, Groq (LLaMA 3.3)
- **Frontend:** React 18, TailwindCSS, Vite
- **Auth:** JWT + bcrypt
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2)

## Setup
See `/backend/.env.example` and `/frontend/vite.config.js`

## Team
Built for Jatayu Season 5 — Use Case 2
