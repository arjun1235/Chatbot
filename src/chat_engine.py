import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from src.load_kb import KnowledgeBase
from src.ticket_manager import TicketManager


class ChatEngine:

    def __init__(self):

        print("Loading AI model...")

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        print("Loading Knowledge Base...")

        self.kb = KnowledgeBase("data/knowledge_base.json")

        self.questions = self.kb.get_questions()

        self.answers = self.kb.get_answers()
        self.ticket_manager = TicketManager()

        print("Creating embeddings...")

        self.embeddings = self.model.encode(
            self.questions,
            convert_to_numpy=True
        )

        print("Ready!\n")

    def ask(self, user_question):

        query_embedding = self.model.encode(
            [user_question],
            convert_to_numpy=True
        )

        similarities = cosine_similarity(
            query_embedding,
            self.embeddings
        )[0]

        best_match = np.argmax(similarities)

        confidence = float(similarities[best_match])

        if confidence >= 0.60:

            return {
                "success": True,
                "answer": self.answers[best_match],
                "confidence": round(confidence, 2)
            }

        ticket_id = self.ticket_manager.create(
            user_question,
            confidence
        )

        return {
            "success": False,
            "ticket": ticket_id,
            "confidence": round(confidence, 2)
        }