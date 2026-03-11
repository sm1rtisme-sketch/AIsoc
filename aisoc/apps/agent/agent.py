import logging
from typing import Dict, Any, Optional, List
from apps.core.config import get_config

logger = logging.getLogger(__name__)


class Agent:
    def __init__(self, config):
        self.config = config
        self.client = None
        self._init_client()

    def _init_client(self):
        try:
            import openai
            openai.api_key = self.config.config.openai.api_key
            openai.base_url = self.config.config.openai.base_url
            self.client = openai
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")

    def chat(self, conversation_id: str, message: str, role: str = 'default') -> Dict[str, Any]:
        if not self.client:
            return {'error': 'OpenAI client not initialized'}

        try:
            response = self.client.chat.completions.create(
                model=self.config.config.openai.model,
                messages=[{'role': 'user', 'content': message}],
            )
            return {
                'message': response.choices[0].message.content,
                'conversation_id': conversation_id,
            }
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return {'error': str(e)}

    def stream_chat(self, conversation_id: str, message: str, role: str = 'default'):
        if not self.client:
            yield {'error': 'OpenAI client not initialized'}
            return

        try:
            response = self.client.chat.completions.create(
                model=self.config.config.openai.model,
                messages=[{'role': 'user', 'content': message}],
                stream=True,
            )
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield {'content': chunk.choices[0].delta.content}
        except Exception as e:
            logger.error(f"Stream chat error: {e}")
            yield {'error': str(e)}
