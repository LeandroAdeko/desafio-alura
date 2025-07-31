import os
import json
import logging
import google.generativeai as genai
from pydantic import BaseModel

class ClassificacaoComentario(BaseModel):
    classificacao: str
    confianca: float

class Gemini:
    def __init__(self, api_key=None, model="gemini-2.0-flash"):
        self.model_name = os.environ.get("GEMINI_MODEL") or model
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.model = self.connect()
        

    def connect(self):
        """Connects to the Gemini API using the API key from the .env file."""

        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(self.model_name)

        return model

    def ask(self, prompt):
        response = self.model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=ClassificacaoComentario,
            ),
        )
        return response.text
    
    def classify_comment(self, comment):
        prompt = f"""Você é um classificador de comentários sobre artistas, álbuns e shows.  
Sua tarefa é analisar o comentário fornecido e classificá-lo em UMA das seguintes categorias:

- ELOGIO → O comentário expressa apreciação, admiração ou algo positivo.  
- CRITICA → O comentário expressa insatisfação, reclamação ou algo negativo.  
- SUGESTAO → O comentário dá uma ideia ou recomendação para melhorar algo.  
- DUVIDA → O comentário faz uma pergunta ou demonstra incerteza sobre algo.  
- SPAM → O comentário não tem relação com o conteúdo ou é autopromoção, golpe ou propaganda.

Retorne um json com a categoria correta e uma porcentagem de confiaça como no exemplo a seguir:

Comentário: "{comment}"
Resposta:"""
        
        response = self.ask(prompt)
        
        return ClassificacaoComentario(**json.loads(response))
