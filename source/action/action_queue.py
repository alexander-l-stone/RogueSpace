from source.action.action import Action
import heapq

class ActionQueue:
    """
    Class for holding all the actions characters currently want to execute
    """
    def __init__(self):
        self.heap:list = []
        self.player_actions_count:int = 0
        heapq.heapify(self.heap)

    def push(self, action:Action):
        """
        Append an action to the queue
        This always assumes action is an Action
        """

        try:
            if(action.originator.flags['is_player'] == True):
                self.player_actions_count += 1
        except(AttributeError):
            pass
        except(KeyError):
            pass
        heapq.heappush(self.heap, action)

    def pop(self):
        """
        Take the top item of the queue
        """
        if len(self.heap) != 0:
            return heapq.heappop(self.heap)
    
    def resolve_actions(self, time):
        action_list = []
        while len(self.heap) > 0 and self.heap[0].time <= time:
            action_list.append(self.pop())
        result_list = []
        for action in action_list:
            try:
                if(action.originator.flags['is_player'] == True):
                    self.player_actions_count -= 1
            except(AttributeError):
                pass
            except(KeyError):
                pass
            result_list.append(action.resolve_action())
        return result_list