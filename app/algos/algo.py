class Algo:
    def __init__(self, time_frame, proximity=[], diversity=[]):
        self.time_frame = time_frame
        self.proximity = proximity
        self.diversity = diversity

    @property
    def name(self):
        raise NotImplementedError
    
    @property
    def extra(self):
        return "No extra information"

    @property
    def attributes(self):
        return ['mass_1', 'lumin_1']
        # Reimplement when functional
        return [
            a for a in self.proximity + self.diversity
        ]
    
    def initialize(self):
        """Retrieve and store the data we will use"""
        raise NotImplementedError

    def process(self):
        """Run algorithm on data"""
        raise NotImplementedError

    def get_plot(self):
        """Return matplot"""
        raise NotImplementedError