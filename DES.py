import queue
import random

class Event:
    def __init__(self, id, end_time, action):
        self.proc_id = id
        self.time = end_time
        self.action = action

    def __str__(self):
        return "A particle({}) {} at {}.".format(self.proc_id, self.action, self.time)

    def __lt__(self, other):
        return self.time < other.time

def ParticleProcess(id, decay_time, start_time = 0):
    time = start_time
    time = yield Event(id, time, "created")
    time = yield Event(id, time + decay_time, "anihilated")

def controller(particles, times=None):
    processes = {}
    events = queue.PriorityQueue()
    if times is not None and len(times) == particles:
        particle_decay_times = list(times)
    else:
        particle_decay_times = [random.randrange(10) for i in range(particles)]
    
    for id, time in zip(range(particles), particle_decay_times):
        tempProc =  ParticleProcess(id, time, id*3)
        events.put(next(tempProc))
        processes[id] = tempProc
        glob_time = 0
        while not events.empty():
            currEvent = events.get()
            print("[{}]".format(glob_time), currEvent)
            glob_time = max(currEvent.time, glob_time)
            try:
                newEv = processes[currEvent.proc_id].send(glob_time)
            except StopIteration:
                del processes[currEvent.proc_id]
            else:
                events.put(newEv)
        
