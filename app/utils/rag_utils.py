import os
import json
import numpy as np
import faiss
from typing import List, Dict, Any, Optional
from openai import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from utils.logging_utils import default_logger as logger

class RAGSystem:
    def __init__(self):
        """Initialize the RAG system with OpenAI embeddings and FAISS index"""
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            logger.error("OpenAI API key not found in environment variables")
            raise ValueError("OpenAI API key is required for RAG functionality")
        
        self.client = OpenAI(api_key=self.openai_api_key)
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        self.index = None
        self.documents = []
        self.metadata = []
        
    def process_documents(self, resume_text: str, jd_text: str, github_data: Optional[Dict] = None) -> None:
        """
        Process and chunk documents for RAG
        
        Args:
            resume_text: Extracted text from resume
            jd_text: Job description text
            github_data: Optional GitHub repository data
        """
        logger.info("Processing documents for RAG system")
        
        # Prepare documents with metadata
        documents = []
        
        # Resume document
        resume_chunks = self.text_splitter.split_text(resume_text)
        for i, chunk in enumerate(resume_chunks):
            documents.append({
                'text': chunk,
                'metadata': {
                    'source': 'resume',
                    'chunk_id': i,
                    'type': 'resume_section'
                }
            })
        
        # Job description document
        jd_chunks = self.text_splitter.split_text(jd_text)
        for i, chunk in enumerate(jd_chunks):
            documents.append({
                'text': chunk,
                'metadata': {
                    'source': 'job_description',
                    'chunk_id': i,
                    'type': 'jd_section'
                }
            })
        
        # GitHub data if available
        if github_data and github_data.get('repositories'):
            for repo in github_data['repositories']:
                repo_text = f"Repository: {repo.get('name', 'Unknown')}\n"
                repo_text += f"Description: {repo.get('description', 'No description')}\n"
                repo_text += f"Language: {repo.get('language', 'Unknown')}\n"
                repo_text += f"Stars: {repo.get('stargazers_count', 0)}\n"
                repo_text += f"URL: {repo.get('html_url', 'No URL')}\n"
                
                if repo.get('topics'):
                    repo_text += f"Topics: {', '.join(repo['topics'])}\n"
                
                repo_chunks = self.text_splitter.split_text(repo_text)
                for i, chunk in enumerate(repo_chunks):
                    documents.append({
                        'text': chunk,
                        'metadata': {
                            'source': 'github',
                            'repo_name': repo.get('name', 'Unknown'),
                            'chunk_id': i,
                            'type': 'github_repo'
                        }
                    })
        
        self.documents = documents
        logger.info(f"Processed {len(documents)} document chunks")
        
    def create_embeddings_and_index(self) -> None:
        """Create embeddings and build FAISS index"""
        if not self.documents:
            logger.error("No documents to process")
            return
        
        logger.info("Creating embeddings and building FAISS index")
        
        # Extract texts and metadata
        texts = [doc['text'] for doc in self.documents]
        self.metadata = [doc['metadata'] for doc in self.documents]
        
        # Create embeddings
        try:
            embeddings_list = self.embeddings.embed_documents(texts)
            embeddings_array = np.array(embeddings_list).astype('float32')
            
            # Create FAISS index
            dimension = embeddings_array.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(embeddings_array)
            
            logger.info(f"Created FAISS index with {len(embeddings_array)} vectors of dimension {dimension}")
            
        except Exception as e:
            logger.error(f"Error creating embeddings: {str(e)}")
            raise
    
    def retrieve_relevant_context(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant context for a given query
        
        Args:
            query: The search query
            top_k: Number of top results to return
            
        Returns:
            List of relevant documents with their metadata
        """
        if not self.index:
            logger.error("FAISS index not initialized")
            return []
        
        try:
            # Create query embedding
            query_embedding = self.embeddings.embed_query(query)
            query_vector = np.array([query_embedding]).astype('float32')
            
            # Search the index
            distances, indices = self.index.search(query_vector, top_k)
            
            # Retrieve relevant documents
            relevant_docs = []
            for idx in indices[0]:
                if idx < len(self.documents):
                    relevant_docs.append({
                        'text': self.documents[idx]['text'],
                        'metadata': self.documents[idx]['metadata'],
                        'score': float(distances[0][list(indices[0]).index(idx)])
                    })
            
            logger.info(f"Retrieved {len(relevant_docs)} relevant documents for query: {query}")
            return relevant_docs
            
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            return []
    
    def generate_rag_response(self, query: str, context_docs: List[Dict[str, Any]]) -> str:
        """
        Generate a response using RAG with retrieved context
        
        Args:
            query: The user query
            context_docs: Retrieved relevant documents
            
        Returns:
            Generated response string
        """
        if not context_docs:
            return "I don't have enough context to answer your question. Please try rephrasing or ask about your resume, job description, or GitHub projects."
        
        # Prepare context
        context_text = "\n\n".join([doc['text'] for doc in context_docs])
        
        # Create prompt with context
        prompt = f"""Based on the following context from the user's resume, job description, and GitHub data, please answer the question.

Context:
{context_text}

Question: {query}

Please provide a comprehensive and helpful answer based on the available context. If the context doesn't contain enough information to fully answer the question, acknowledge this and provide what insights you can.

Answer:"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant that analyzes resumes, job descriptions, and GitHub profiles to provide career advice and insights."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating RAG response: {str(e)}")
            return f"Sorry, I encountered an error while generating a response: {str(e)}"
    
    def chat_with_rag(self, user_message: str) -> str:
        """
        Complete RAG pipeline: retrieve context and generate response
        
        Args:
            user_message: User's question or message
            
        Returns:
            Generated response
        """
        # Retrieve relevant context
        context_docs = self.retrieve_relevant_context(user_message, top_k=5)
        
        # Generate response
        response = self.generate_rag_response(user_message, context_docs)
        
        return response 