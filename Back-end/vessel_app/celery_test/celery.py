import os
import celery

@celery.task ## Task to be run at a later time 
def add(x, y): #  either signaled by a user or an event 
    return x + y


task = add.delay(1, 2)
task.result = 3

os.system("pause")