#!/usr/bin/env python3
"""
Moses Omondi AI Assistant - Minimal Lambda Version
Simple FastAPI service for AWS Lambda deployment
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import json

# API Models
class QueryRequest(BaseModel):
    question: str
    context_count: int = 5
    include_sources: bool = True

class QueryResponse(BaseModel):
    answer: str
    processing_time: float
    sources_used: int
    timestamp: str
    query: str

class HealthResponse(BaseModel):
    status: str
    version: str
    message: str

# Initialize FastAPI app
app = FastAPI(
    title="Moses Omondi AI Assistant API",
    description="DevSecOps and AI Engineering expertise API - Lambda Version",
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

@app.get("/", response_model=dict)
async def root():
    """Root endpoint with welcome message"""
    return {
        "message": "Moses Omondi AI Assistant API",
        "description": "DevSecOps and AI Engineering expertise at your fingertips",
        "version": "1.0.0",
        "status": "🚀 Running on AWS Lambda",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "query": "/query",
            "expertise": "/expertise"
        },
        "contact": {
            "linkedin": "https://linkedin.com/in/moses-omondi",
            "github": "https://github.com/Moses-Omondi"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        message="Moses AI Assistant is running successfully on AWS Lambda!"
    )

@app.get("/expertise", response_model=dict)
async def get_expertise_summary():
    """Get a summary of Moses's professional expertise"""
    return {
        "expertise_summary": "Moses Omondi is a DevSecOps and AI Engineering expert",
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
        "experience": {
            "devsecops": "CI/CD pipeline security, SAST/DAST integration, security automation",
            "cloud": "AWS security architecture, Infrastructure as Code, compliance frameworks",
            "ai_ml": "MLOps, model security, AI pipeline automation, fine-tuning",
            "kubernetes": "Pod security, RBAC, network policies, cluster hardening"
        },
        "contact": {
            "linkedin": "https://linkedin.com/in/moses-omondi",
            "github": "https://github.com/Moses-Omondi"
        }
    }

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
    start_time = datetime.now()
    
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    # Generate response based on question content
    answer = generate_expert_response(request.question)
    
    processing_time = (datetime.now() - start_time).total_seconds()
    
    return QueryResponse(
        answer=answer,
        processing_time=processing_time,
        sources_used=1,
        timestamp=datetime.now().isoformat(),
        query=request.question
    )

def generate_expert_response(question: str) -> str:
    """Generate expert response based on Moses's knowledge areas"""
    question_lower = question.lower()
    
    # DevSecOps related questions
    if any(keyword in question_lower for keyword in ['devsecops', 'ci/cd', 'pipeline', 'security']):
        return """Based on Moses Omondi's DevSecOps expertise:

**Key Security Practices:**
• Implement SAST/DAST scanning in CI/CD pipelines
• Use secure secrets management (HashiCorp Vault, AWS Secrets Manager)
• Implement branch protection rules and code review processes
• Automated security testing at each pipeline stage

**Recommendations:**
• Shift-left security approach - integrate security early in development
• Use Infrastructure as Code (IaC) with security scanning
• Implement zero-trust architecture principles
• Regular vulnerability assessments and penetration testing

**Tools & Technologies:**
• SonarQube, Snyk, OWASP ZAP for security scanning
• Jenkins, GitLab CI, GitHub Actions for pipeline automation
• Docker security scanning with Trivy or Clair
• Kubernetes security with Pod Security Standards

*This response reflects Moses Omondi's experience in DevSecOps and security engineering.*"""

    # Kubernetes related questions  
    elif any(keyword in question_lower for keyword in ['kubernetes', 'k8s', 'container']):
        return """Based on Moses Omondi's Kubernetes security expertise:

**Security Best Practices:**
• Implement Role-Based Access Control (RBAC)
• Use Pod Security Standards and Network Policies
• Regular container image scanning for vulnerabilities
• Enable audit logging and monitoring

**Container Security:**
• Use minimal base images and multi-stage builds
• Run containers as non-root users
• Implement resource limits and requests
• Regular security updates and patching

**Cluster Hardening:**
• Secure etcd with encryption at rest
• Use admission controllers for policy enforcement
• Network segmentation with Calico or Cilium
• Regular backup and disaster recovery testing

*Based on Moses Omondi's experience with Kubernetes security and orchestration.*"""

    # AWS/Cloud related questions
    elif any(keyword in question_lower for keyword in ['aws', 'cloud', 'lambda', 'ec2']):
        return """Based on Moses Omondi's AWS and Cloud Architecture expertise:

**AWS Security Best Practices:**
• Follow AWS Well-Architected Security Pillar
• Implement least privilege IAM policies
• Enable CloudTrail, GuardDuty, and Config
• Use AWS Security Hub for centralized monitoring

**Infrastructure Security:**
• Infrastructure as Code with CloudFormation/CDK
• VPC security with proper network segmentation  
• Encrypt data at rest and in transit
• Regular security assessments and compliance audits

**Cost Optimization:**
• Use serverless architecture (Lambda, API Gateway)
• Implement auto-scaling and right-sizing
• Reserved instances for predictable workloads
• Regular cost monitoring and optimization

*This reflects Moses Omondi's experience with AWS security and cloud architecture.*"""

    # AI/ML related questions
    elif any(keyword in question_lower for keyword in ['ai', 'ml', 'machine learning', 'model']):
        return """Based on Moses Omondi's AI/ML Engineering expertise:

**MLSecOps Practices:**
• Secure ML pipeline development and deployment
• Model governance and version control
• Data privacy and protection in ML workflows
• Automated model testing and validation

**AI Security:**
• Protect against adversarial attacks
• Implement model explainability and transparency
• Secure data preprocessing and feature engineering
• Monitor for model drift and bias

**Technical Implementation:**
• PyTorch and TensorFlow for model development
• MLflow for experiment tracking and model registry
• Kubernetes for scalable ML workload orchestration
• CI/CD pipelines for automated model deployment

*Based on Moses Omondi's experience in AI/ML engineering and MLSecOps.*"""

    # General technical questions
    else:
        return f"""Based on Moses Omondi's technical expertise, here's guidance on: "{question}"

**Professional Background:**
Moses Omondi is a DevSecOps engineer and AI/ML specialist with expertise in:
• Secure software development lifecycle
• Cloud architecture and security (AWS, Azure)
• Full-stack development (MERN, Spring Boot)
• AI/ML pipeline development and deployment

**General Recommendations:**
• Security-first approach in all implementations
• Automated testing and continuous integration
• Documentation and knowledge sharing
• Regular security reviews and updates

**Technologies & Tools:**
• Programming: Python, Java, JavaScript, TypeScript
• Cloud: AWS, Docker, Kubernetes
• AI/ML: PyTorch, TensorFlow, MLflow
• Security: SAST/DAST tools, vulnerability scanning

For more specific guidance, please ask about DevSecOps, AWS, Kubernetes, or AI/ML topics.

*This response is based on Moses Omondi's documented professional experience.*"""

# Lambda handler
from mangum import Mangum
handler = Mangum(app)

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Moses Omondi AI Assistant API...")
    print("📍 API will be available at: http://localhost:8000")
    print("📖 Documentation at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
