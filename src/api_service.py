#!/usr/bin/env python3
"""
Moses Omondi AI Assistant API Service
Professional FastAPI wrapper for the DevSecOps AI Assistant

Usage:
    uvicorn src.api_service:app --host 0.0.0.0 --port 8000
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import time
import asyncio
from datetime import datetime

from src.rag_system import DevSecOpsRAG

# API Models
class QueryRequest(BaseModel):
    question: str
    context_count: int = 5
    include_sources: bool = True

class Source(BaseModel):
    content: str
    metadata: dict
    relevance_score: float

class QueryResponse(BaseModel):
    answer: str
    processing_time: float
    sources_used: int
    timestamp: str
    sources: Optional[List[Source]] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    knowledge_base_status: str
    total_documents: int

class SystemStats(BaseModel):
    total_queries: int
    average_response_time: float
    knowledge_base_size: int
    categories: List[str]

# Initialize FastAPI app
app = FastAPI(
    title="Moses Omondi AI Assistant API",
    description="Professional DevSecOps and AI Engineering expertise API",
    version="1.0.0",
    contact={
        "name": "Moses Omondi",
        "url": "https://linkedin.com/in/moses-omondi",
        "email": "contact@moses-omondi.dev"
    }
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for tracking
query_count = 0
total_response_time = 0.0
rag_system = None

@app.on_event("startup")
async def startup_event():
    """Initialize the RAG system on startup"""
    global rag_system
    print("🚀 Initializing Moses Omondi AI Assistant...")
    rag_system = DevSecOpsRAG()
    print("✅ AI Assistant ready for queries!")

@app.get("/", response_model=dict)
async def root():
    """Root endpoint with welcome message"""
    return {
        "message": "Moses Omondi AI Assistant API",
        "description": "DevSecOps and AI Engineering expertise at your fingertips",
        "version": "1.0.0",
        "docs": "/docs",
        "linkedin": "https://linkedin.com/in/moses-omondi",
        "github": "https://github.com/Moses-Omondi"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        knowledge_info = rag_system.get_knowledge_base_info()
        return HealthResponse(
            status="healthy",
            version="1.0.0",
            knowledge_base_status="active",
            total_documents=knowledge_info.get('total_documents', 0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.get("/stats", response_model=SystemStats)
async def get_system_stats():
    """Get system statistics"""
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    knowledge_info = rag_system.get_knowledge_base_info()
    avg_response_time = total_response_time / query_count if query_count > 0 else 0.0
    
    return SystemStats(
        total_queries=query_count,
        average_response_time=avg_response_time,
        knowledge_base_size=knowledge_info.get('total_documents', 0),
        categories=knowledge_info.get('categories', [])
    )

@app.post("/query", response_model=QueryResponse)
async def query_assistant(request: QueryRequest):
    """
    Query Moses Omondi's AI Assistant
    
    This endpoint provides access to Moses's professional expertise in:
    - DevSecOps and Security Engineering
    - Full-Stack Development (MERN, Spring Boot)
    - AI/ML Engineering and Fine-tuning
    - Cloud Architecture (AWS, Azure)
    - Academic Research and Education
    """
    global query_count, total_response_time
    
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        # Process the query
        result = rag_system.query(request.question, request.context_count)
        
        # Update statistics
        query_count += 1
        total_response_time += result['processing_time']
        
        # Prepare sources if requested
        sources = None
        if request.include_sources:
            sources = [
                Source(
                    content=ctx['content'][:500] + "..." if len(ctx['content']) > 500 else ctx['content'],
                    metadata=ctx['metadata'],
                    relevance_score=ctx['relevance_score']
                )
                for ctx in result['contexts']
            ]
        
        return QueryResponse(
            answer=result['answer'],
            processing_time=result['processing_time'],
            sources_used=result['sources_used'],
            timestamp=datetime.now().isoformat(),
            sources=sources
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")

@app.get("/expertise", response_model=dict)
async def get_expertise_summary():
    """Get a summary of Moses's professional expertise"""
    if not rag_system:
        raise HTTPException(status_code=503, detail="RAG system not initialized")
    
    try:
        summary = rag_system.get_expertise_summary()
        return {
            "expertise_summary": summary,
            "specializations": [
                "DevSecOps Engineering",
                "Full-Stack Development",
                "AI/ML Engineering", 
                "Cloud Architecture",
                "Academic Research"
            ],
            "technologies": [
                "Python", "Java", "JavaScript", "React", "Spring Boot",
                "AWS", "Docker", "Kubernetes", "PyTorch", "TensorFlow"
            ],
            "linkedin": "https://linkedin.com/in/moses-omondi",
            "github": "https://github.com/Moses-Omondi"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get expertise summary: {str(e)}")

# Specialized endpoints for different query types
@app.post("/query/technical", response_model=QueryResponse)
async def query_technical(request: QueryRequest):
    """Specialized endpoint for technical questions"""
    enhanced_question = f"From a technical implementation perspective: {request.question}"
    request.question = enhanced_question
    return await query_assistant(request)

@app.post("/query/career", response_model=QueryResponse) 
async def query_career(request: QueryRequest):
    """Specialized endpoint for career-related questions"""
    enhanced_question = f"Regarding Moses's professional background and career: {request.question}"
    request.question = enhanced_question
    return await query_assistant(request)

@app.post("/query/projects", response_model=QueryResponse)
async def query_projects(request: QueryRequest):
    """Specialized endpoint for project-related questions"""
    enhanced_question = f"About Moses's projects and implementations: {request.question}"
    request.question = enhanced_question
    return await query_assistant(request)

# Lambda handler
from mangum import Mangum
handler = Mangum(app)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Moses Omondi AI Assistant API...")
    print("📍 API will be available at: http://localhost:8000")
    print("📖 Documentation at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
