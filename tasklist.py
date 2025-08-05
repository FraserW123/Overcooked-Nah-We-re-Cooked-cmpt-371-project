import random
class TaskList:
    def __init__(self):
        self.tasks = []
        

    def get_tasklist(self, amount=5):

        if self.tasks:
            return self.tasks
        possible_tasks = ['h', 'z','s'] # 'h' for hamburger, 'z' for pizza, 's' for sushi
        for _ in range(amount):
            task = random.choice(possible_tasks) # if we want to select a random task
            # task = possible_tasks[0]
            self.tasks.append(task)
        return self.tasks

    def mark_completed(self, task):
        # if food is in the task list, mark it as completed and return True, False o/w
        if task in self.tasks:
            index = self.tasks.index(task)
            self.tasks[index] = "completed"
            return True  
        return False
    
    def check_completed(self):
        if all(task == "completed" for task in self.tasks):
            return "True"
        return ""
    
    def create_string(self):
        return ', '.join(self.tasks)