from database.database import Database


class TicketManager:

    def __init__(self):

        self.db = Database()

    def create(self, issue, confidence):

        ticket_id = self.db.create_ticket(

            issue,
            confidence
        )

        return ticket_id