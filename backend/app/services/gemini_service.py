from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from app.config import settings
from typing import Type, TypeVar
from pydantic import BaseModel
import json

T = TypeVar('T', bound=BaseModel)


class GeminiService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.7,
            convert_system_message_to_human=True
        )

        self.llm_structured = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.7,
            convert_system_message_to_human=True
        )

    async def generate_structured(self, prompt: str, response_model: Type[T]) -> T:
        """Generate structured output using Pydantic model"""
        try:
            parser = PydanticOutputParser(pydantic_object=response_model)

            prompt_template = PromptTemplate(
                template="{prompt}\n\n{format_instructions}",
                input_variables=["prompt"],
                partial_variables={"format_instructions": parser.get_format_instructions()}
            )

            formatted_prompt = prompt_template.format(prompt=prompt)
            response = await self.llm_structured.ainvoke(formatted_prompt)

            # Parse the response
            parsed = parser.parse(response.content)
            return parsed

        except Exception as e:
            print(f"Error in structured generation: {str(e)}")
            raise

    async def generate_text(self, prompt: str) -> str:
        """Generate plain text response"""
        try:
            response = await self.llm.ainvoke(prompt)
            return response.content
        except Exception as e:
            print(f"Error in text generation: {str(e)}")
            raise


# Singleton instance
gemini_service = GeminiService()
