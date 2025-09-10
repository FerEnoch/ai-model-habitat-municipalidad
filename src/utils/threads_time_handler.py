class ThreadsTimeHandler:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start_timer(self):
        self.start_time = datetime.now()

    def stop_timer(self):
        self.end_time = datetime.now()

    def get_elapsed_time(self):
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0