class Location:
    def __init__(self):
        self.visitors=0

    def add_visitor(self):
        self.visitors+=1

    def remove_visitor(self):
        self.visitor-=1
