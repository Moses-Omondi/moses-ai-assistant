#!/usr/bin/env python3
"""
RAG System for Moses's DevSecOps AI Assistant

Core system that handles:
- Document retrieval from ChromaDB
- Context preparation for LLM
- Query processing with Ollama
- Response generation with citations
"""

import logging
import time
from typing import List, Dict, Any, Optional
from pathlib import Path
import chromadb
from langchain_community.embeddings import HuggingFaceEmbeddings
# Note: Ollama not available in Lambda - using fallback response system
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DevSecOpsRAG:
    """
    Retrieval-Augmented Generation system specialized for DevSecOps and AI Engineering
    Uses Moses's professional knowledge to provide expert-level responses
    """
    
    def __init__(self, db_path: str = None, model_name: str = "llama3.2:latest"):
        if db_path is None:
            db_path = str(Path(__file__).parent.parent / "data" / "chroma_db")
        self.db_path = Path(db_path)
        self.model_name = model_name
        
        # Initialize embeddings (same as document processor for consistency)
        logger.info("Initializing embeddings model...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        # Initialize ChromaDB connection
        logger.info("Connecting to knowledge base...")
        self.client = chromadb.PersistentClient(path=str(self.db_path))
        
        # Connect to Moses's knowledge collection
        self.collection_name = "moses_devsecops_knowledge"
        try:
            self.collection = self.client.get_collection(self.collection_name)
            logger.info(f"Connected to knowledge base: {self.collection_name}")
        except Exception as e:
            logger.error(f"Could not connect to knowledge base: {e}")
            raise Exception("Knowledge base not found. Please run document_processor.py first.")
        
        # System prompt - this defines Moses's AI personality
        self.system_prompt = f"""You are Moses Omondi's AI assistant, an expert in DevSecOps, CI/CD security, MLOps, and AI Engineering.

EXPERTISE AREAS:
- DevSecOps: Security integration in development workflows
- CI/CD Security: Pipeline security, SAST/DAST, secure deployments
- Kubernetes Security: Pod security, RBAC, network policies, admission controllers
- AWS Security: SO3 compliance, IAM, security services, cloud architecture
- MLOps/MLSecOps: Secure ML pipelines, model governance, AI security
- Infrastructure Security: Infrastructure as Code, container security, monitoring

RESPONSE STYLE:
- Professional and authoritative (you represent Moses's expertise)
- Provide specific, actionable technical guidance
- Include security-first recommendations
- Reference best practices and industry standards
- Use concrete examples when helpful
- Be concise but comprehensive

IMPORTANT:
- Base responses on Moses's documented experience and knowledge
- When uncertain, acknowledge limitations rather than guess
- Focus on practical, implementable solutions
- Emphasize security considerations in all recommendations
"""

    def retrieve_context(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant context from Moses's knowledge base
        Returns the most relevant document chunks for the query
        """
        logger.info(f"Retrieving context for query: {query[:100]}...")
        
        try:
            # Query the collection for relevant documents
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                include=['documents', 'metadatas', 'distances']
            )
            
            contexts = []
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    context = {
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'relevance_score': 1 - results['distances'][0][i]  # Convert distance to similarity
                    }
                    contexts.append(context)
                    
            logger.info(f"Retrieved {len(contexts)} relevant contexts")
            return contexts
            
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return []
    
    def prepare_context_string(self, contexts: List[Dict[str, Any]]) -> str:
        """
        Format retrieved contexts into a string for the LLM
        """
        if not contexts:
            return "No relevant context found in Moses's knowledge base."
        
        context_string = "RELEVANT KNOWLEDGE FROM MOSES'S EXPERTISE:\\n\\n"
        
        for i, ctx in enumerate(contexts, 1):
            category = ctx['metadata'].get('category', 'general').replace('_', ' ').title()
            source = Path(ctx['metadata'].get('source', 'Unknown')).name
            
            context_string += f"[Source {i} - {category}] ({source}):\\n"
            context_string += f"{ctx['content']}\\n\\n"
        
        return context_string
    
    def generate_response(self, query: str, context: str) -> str:
        """
        Generate response based on retrieved context (Lambda-compatible version)
        """
        logger.info("Generating response from knowledge base...")
        
        try:
            # Extract the most relevant information from context
            if "No relevant context" in context:
                return "I don't have specific information about that topic in Moses Omondi's knowledge base. Please try a more specific question about DevSecOps, CI/CD security, AWS, Kubernetes, or AI/ML engineering."
            
            # Create a structured response based on the context
            response = f"""Based on Moses Omondi's expertise, here's what I can tell you about your question: "{query}"

**Key Information:**
{self._extract_key_points(context)}

**Practical Recommendations:**
{self._generate_recommendations(query, context)}

**Security Considerations:**
{self._extract_security_points(context)}

*This response is based on Moses Omondi's documented experience in DevSecOps, AI Engineering, and Cloud Architecture.*
"""
            
            logger.info(f"Generated response ({len(response)} characters)")
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"I apologize, but I encountered an error processing your question. Please try rephrasing your query. Error: {str(e)}"
    
    def _extract_key_points(self, context: str) -> str:
        """Extract key points from the context"""
        lines = context.split('\\n')
        key_points = []
        
        for line in lines:
            if line.strip() and not line.startswith('RELEVANT KNOWLEDGE') and not line.startswith('[Source'):
                # Take first few sentences that contain useful information
                if any(keyword in line.lower() for keyword in ['security', 'implement', 'deploy', 'configure', 'best practice']):
                    key_points.append(f"• {line.strip()[:200]}")
                    if len(key_points) >= 3:
                        break
        
        return '\n'.join(key_points) if key_points else "• Relevant technical documentation and implementation guides available"
    
    def _generate_recommendations(self, query: str, context: str) -> str:
        """Generate practical recommendations based on query and context"""
        query_lower = query.lower()
        
        if 'kubernetes' in query_lower or 'k8s' in query_lower:
            return "• Implement RBAC and network policies\n• Use Pod Security Standards\n• Regular security scanning of container images\n• Monitor cluster activity with audit logging"
        elif 'ci/cd' in query_lower or 'pipeline' in query_lower:
            return "• Integrate SAST/DAST tools in pipeline\n• Use secure secrets management\n• Implement branch protection rules\n• Automated security testing at each stage"
        elif 'aws' in query_lower or 'cloud' in query_lower:
            return "• Follow AWS Well-Architected Security Pillar\n• Implement least privilege IAM policies\n• Enable CloudTrail and GuardDuty\n• Use AWS Config for compliance monitoring"
        elif 'ai' in query_lower or 'ml' in query_lower or 'model' in query_lower:
            return "• Implement MLSecOps practices\n• Secure model training pipelines\n• Monitor for model drift and bias\n• Protect sensitive training data"
        else:
            return "• Follow security-first development practices\n• Implement proper monitoring and logging\n• Regular security assessments and updates\n• Documentation and knowledge sharing"
    
    def _extract_security_points(self, context: str) -> str:
        """Extract security-related points from context"""
        security_keywords = ['security', 'secure', 'vulnerability', 'threat', 'risk', 'compliance', 'audit']
        lines = context.split('\\n')
        security_points = []
        
        for line in lines:
            if any(keyword in line.lower() for keyword in security_keywords):
                clean_line = line.strip()
                if clean_line and not clean_line.startswith('[Source'):
                    security_points.append(f"• {clean_line[:150]}")
                    if len(security_points) >= 2:
                        break
        
        return '\n'.join(security_points) if security_points else "• Always prioritize security in implementation\n• Regular security reviews and updates recommended"
    
    def query(self, question: str, n_contexts: int = 5) -> Dict[str, Any]:
        """
        Main query method - orchestrates the entire RAG process
        """
        start_time = time.time()
        logger.info(f"Processing query: {question[:100]}...")
        
        # Step 1: Retrieve relevant context
        contexts = self.retrieve_context(question, n_contexts)
        
        # Step 2: Prepare context for LLM
        context_string = self.prepare_context_string(contexts)
        
        # Step 3: Generate response
        answer = self.generate_response(question, context_string)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Prepare result
        result = {
            'answer': answer,
            'contexts': contexts,
            'sources_used': len(contexts),
            'processing_time': processing_time,
            'query': question
        }
        
        logger.info(f"Query processed successfully in {processing_time:.2f} seconds")
        return result
    
    def get_knowledge_base_info(self) -> Dict[str, Any]:
        """
        Get information about the knowledge base
        """
        try:
            count = self.collection.count()
            
            # Get sample documents to understand categories
            sample_results = self.collection.get(limit=100, include=['metadatas'])
            categories = set()
            
            if sample_results['metadatas']:
                for metadata in sample_results['metadatas']:
                    if 'category' in metadata:
                        categories.add(metadata['category'])
            
            return {
                'total_documents': count,
                'categories': sorted(list(categories)),
                'status': 'active'
            }
            
        except Exception as e:
            logger.error(f"Error getting knowledge base info: {e}")
            return {
                'total_documents': 0,
                'categories': [],
                'status': 'error',
                'error': str(e)
            }
    
    def search_by_category(self, query: str, category: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search within a specific category (security, cicd, infrastructure, etc.)
        """
        logger.info(f"Searching in category '{category}' for: {query[:100]}...")
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results * 2,  # Get more results to filter
                where={"category": category},
                include=['documents', 'metadatas', 'distances']
            )
            
            contexts = []
            if results['documents'] and results['documents'][0]:
                for i in range(min(n_results, len(results['documents'][0]))):
                    context = {
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'relevance_score': 1 - results['distances'][0][i]
                    }
                    contexts.append(context)
            
            logger.info(f"Found {len(contexts)} results in category '{category}'")
            return contexts
            
        except Exception as e:
            logger.error(f"Error searching by category: {e}")
            return []
    
    def get_expertise_summary(self) -> str:
        """
        Generate a summary of Moses's expertise based on the knowledge base
        """
        categories_info = self.get_knowledge_base_info()
        
        summary = """Moses Omondi is a DevSecOps and AI Engineering expert with comprehensive knowledge in:

🛡️ **DevSecOps & Security:**
- CI/CD pipeline security and automation
- Infrastructure security and compliance
- Security scanning and vulnerability management
- Zero-trust architecture implementation

☁️ **Cloud & Infrastructure:**
- AWS security and SO3 compliance
- Kubernetes security and best practices
- Container security and orchestration
- Infrastructure as Code (IaC) security

🤖 **AI/ML Engineering:**
- MLOps and MLSecOps implementation
- Model security and governance
- AI pipeline automation
- Machine learning infrastructure

🔧 **Technical Implementation:**
- Secure software development lifecycle
- Automated security testing
- Compliance frameworks and auditing
- Security monitoring and incident response
"""
        
        if categories_info['total_documents'] > 0:
            summary += f"\\n📚 **Knowledge Base:** {categories_info['total_documents']} documented experiences and implementations"
        
        return summary

# Utility functions for testing and debugging
def test_rag_system():
    """Test the RAG system with sample queries"""
    print("🧪 Testing Moses's DevSecOps AI Assistant...")
    
    try:
        rag = DevSecOpsRAG()
        
        # Test queries
        test_queries = [
            "How do I secure a Kubernetes deployment?",
            "What are the best practices for CI/CD security?",
            "How should I implement MLSecOps?",
            "What AWS security controls are needed for compliance?"
        ]
        
        for query in test_queries:
            print(f"\\n❓ Testing: {query}")
            result = rag.query(query)
            print(f"✅ Response generated ({result['sources_used']} sources, {result['processing_time']:.2f}s)")
            print(f"📄 Response preview: {result['answer'][:200]}...")
            
        print(f"\\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_rag_system()
