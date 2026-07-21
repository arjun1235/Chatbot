import json
from pathlib import Path


class KnowledgeBase:

    def __init__(self, filename):

        self.filename = Path(filename)

        self.data = self.load_data()

    def load_data(self):

        with open(self.filename, "r", encoding="utf-8") as file:
            return json.load(file)

    def get_questions(self):

        return [item["question"] for item in self.data]

    def get_answers(self):

        return [item["answer"] for item in self.data]

    def get_categories(self):

        return [item["category"] for item in self.data]