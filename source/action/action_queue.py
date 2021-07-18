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
        """Resolve all the actions in the queue that are at time equal to time or earlier.

        Args:
            time (int): An integer for the time you should advance the queue too.

        Returns:
            list: This will be a list of resolved actions. Should be a list of dictionaries.
        """
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
            for result in action.resolve_action():
                result_list.append(result)
        return result_list