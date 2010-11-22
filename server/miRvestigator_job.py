import datetime

class Job:
    """Represents a task for the miRvestigator server"""
    def __init__(self):
        self.created = datetime.datetime.now()

