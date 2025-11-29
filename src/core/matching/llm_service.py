from openai import OpenAI
from src.core.config.settings import settings
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.client = None
        if settings.OPENAI_API_KEY:
            try:
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
                logger.info("OpenAI client initialized.")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
        else:
            logger.warning("OPENAI_API_KEY not found. LLM service will be disabled.")

    def resolve_conflict(self, candidates: list, input_text: str):
        """
        Uses LLM to choose the best match from candidates.
        candidates: list of (vehicle_id, score)
        input_text: the original text to match
        
        Returns: (vehicle_id, score) or None
        """
        if not self.client:
            logger.warning("LLM client not available.")
            return None

        if not candidates:
            return None

        # Prepare prompt
        # candidates is list of (id, name, score)
        candidates_str = "\n".join([f"- ID: {cid}, Name: {cname}" for cid, cname, _ in candidates])

        logger.info(f"LLM Candidates:\n{candidates_str}")

        prompt = f"""
        You are an expert automotive data analyst. Your task is to match a raw vehicle description (Input) to the correct vehicle in our official catalog (Candidates).

        ### Input Vehicle:
        "{input_text}"

        ### Candidate Matches:
        {candidates_str}

        ### Instructions:
        1. Analyze the Input vs each Candidate Name.
        2. Focus heavily on MAKE and MODEL.
        3. Ignore year differences if they are within +/- 2 years.
        4. Ignore formatting differences (e.g., "Mazda 3" vs "Mazda3", "F-150" vs "F150").
        5. Select the BEST match from the list, even if the description is more detailed than the input.
        6. Only reply "NONE" if the Input is completely different from ALL candidates (e.g. different Make/Model).

        ### Output Format:
        Reply ONLY with the exact ID of the best match. Do not write any other text.
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that matches vehicle names."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0
            )
            
            content = response.choices[0].message.content.strip()
            
            logger.info(f"LLM Raw Response: {content}")
            
            if content == "NONE":
                logger.info("LLM returned NONE")
                return None
            
            # Check if content matches any candidate ID
            for cid, cname, score in candidates:
                if content == cid:
                    logger.info(f"LLM matched candidate: {cid}")
                    return (cid, score)
            
            logger.warning(f"LLM returned '{content}' which is not in candidates: {[c[0] for c in candidates]}")
            return None

        except Exception as e:
            logger.error(f"Error calling LLM: {e}")
            return None

llm_service = LLMService()
