# Name: Evan Miocevich
# Student Number: 24147733

class Leaderboard:
    """A leaderboard of speedrunning record times.

    Each entry has a time in seconds and a runner name.
    Runners may submit multiple runs.
    The leaderboard is ranked fastest run first.
    Ties receive the same rank as each other, so for example if runners submit
    the times 10, 20, 20, and 30, they will have the ranks 1, 2, 2, and 4.
    """
    def binSearch(self, arr, target, type):
            #type 0 for searching by time
            #type for 1 for searching by time then name   
            if type == 0:
                if len(arr) == 2 and arr[0][0] < target < arr[1][0]:
                    return 1
                elif len(arr) == 1:
                    if arr[0][0] < target:
                        return 1
                    else:
                        return 0
                elif len(arr) == 0:
                    return 0
                mid = len(arr)//2
                if target == arr[mid][0]:
                    return len(arr[0:mid])
                if target > arr[mid][0]:
                    return len(arr[0:mid]) + self.binSearch(arr[mid:], target, type)
                elif target < arr[mid][0]:
                    return self.binSearch(arr[0:mid], target, type)
            elif type == 1:
                if len(arr) == 2 and arr[0] < target < arr[1]:
                    return 1
                elif len(arr) == 1:
                    if arr[0] < target:
                        return 1
                    else:
                        return 0
                elif len(arr) == 0:
                    return 0
                mid = len(arr)//2
                if target == arr[mid]:
                    return len(arr[0:mid])
                if target > arr[mid]:
                    return len(arr[0:mid]) + self.binSearch(arr[mid:], target, type)
                elif target < arr[mid]:
                    return self.binSearch(arr[0:mid], target, type)
                
    def __init__(self, runs=[]):
        """Constructs a leaderboard with the given runs.

        The given list of runs is not required to be in order.

        Args:
            runs: Initial leaderboard entries as list of (time, name) pairs.
        """
        def merge(lhs, rhs, L):
            i,j = 0,0
            while i + j < len(L):
                if i == len(lhs):
                    L[i+j] = rhs[j]
                    j += 1
                elif j == len(rhs) or lhs[i] < rhs[j]:
                    L[i+j] = lhs[i]
                    i += 1
                else:
                    L[i+j] = rhs[j]
                    j += 1
        def mergeSort(L):
            n = len(L)
            if n < 2:
                return
            mid = n//2
            L1 = L[0:mid]
            L2 = L[mid:]
            mergeSort(L1)
            mergeSort(L2)
            merge(L1, L2, L)
        #by default, python compares lists of tuples by the first element of each tuple,
        #and then by the next if their first element matches, so no lamba required 
        mergeSort(runs)
        self.leaderboard = runs
        

    def get_runs(self):
        """Returns the current leaderboard.

        Leaderboard is given in rank order, tie-broken by runner name.

        Returns:
            The current leaderboard as a list of (time, name) pairs.
        """
        return self.leaderboard

    def submit_run(self, time, name):
        """Adds the given run to the leaderboard

        Args:
            time: The run time in seconds.
            name: The runner's name.
        """
        index = self.binSearch(self.leaderboard, (time, name), 1)
        self.leaderboard.insert(index, (time, name))
      
    def get_rank_time(self, rank):
        
        """Get the time required to achieve at least a given rank.

        For example, `get_rank_time(5)` will give the maximum possible time
        that would be ranked fifth.

        Args:
            rank: The rank to look up.

        Returns:
            The time required to place `rank`th or better.
        """ 
        return self.leaderboard[rank-1][0]
        
    def get_possible_rank(self, time):
        """Determine what rank the run would get if it was submitted.

        Does not actually submit the run.

        Args:
            time: The run time in seconds.

        Returns:
            The rank this run would be if it were to be submitted.
        """
        ind = self.binSearch(self.leaderboard, time, 0)
        if self.leaderboard[ind][0] != time:
            return ind + 1
        i = 0
        while self.leaderboard[ind-i][0] == time:
            i += 1
            if ind -i < 0:
                return 1
        return ind - i + 2

    def count_time(self, time):
        """Count the number of runs with the given time.

        Args:
            time: The run time to count, in seconds.

        Returns:
            The number of submitted runs with that time.
        """
        #optional algorithm that has an equivalent asymptotic complexity
        '''count = 0
        for i in self.leaderboard:
            if i[0] == time:
                count += 1
            elif i[0] > time:
                break
        return count'''
        
        count = 0
        ind = self.binSearch(self.leaderboard, time, 0)
        if self.leaderboard[ind][0] != time:
            return 0
        i = 0
        while self.leaderboard[ind -i][0] == time:
            count += 1
            i += 1
            if ind - i < 0:
                break
        i = 0
        while self.leaderboard[ind + i][0] == time:
            if i != 0:
                count += 1
            i += 1
            if ind + i == len(self.leaderboard):
                break
        return count