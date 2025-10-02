# Name: Evan Mioceich
# Student Number: 24147733

class Genealogy:
    """The genealogy and succession order for Envoy of the Kiktil."""
    class child:
        def __init__(self, parentName, name):
            self.parentName = parentName
            self.name = name
            self.children = []
            self.level = 0
            
    def __init__(self, originator_name):
        """Constructs an initial genealogy containing no individuals other than
        the Originator.

        Args:
            originator_name: The name of the Originator of the Kiktil species.
        """
        originator = self.child(None, originator_name)
        self.people = {originator_name: originator}
        self.originatorName = originator_name


    def add_child(self, parent_name, child_name):
        """Adds a new child belonging to a given parent.

        You may assume the parent has previously been added as the child of
        another individual, and that no individual named `child_name` exists.

        Target Complexity: O(1) expected.

        Args:
            parent_name: The name of the parent individual.
            child_name: The name of their new child.
        """
        newChild = self.child(parent_name, child_name)
        newChild.level = self.people[parent_name].level + 1
        self.people[parent_name].children.append(child_name)
        self.people[child_name] = newChild
        
    def get_primogeniture_order(self):
        """Returns the primogeniture succession order for Envoy of the Kiktil.

        By primogeniture, succession flows from parent to eldest child, only
        moving to the next youngest sibling after all their elder sibling's
        descendants.

        Target Complexity: O(N), where N is how many indivduals have been added.

        Returns:
            A list of the names of individuals in primogeniture succession order
            starting with the Originator.
        """
        def recurseDown(name):
            Available = []
            finalOrder = []
            child = self.people[name]
            while True:
                if len(child.children) > 1:
                    Available.append(child.children[1:])
                finalOrder.append(child.name)
                if len(child.children) == 0:
                    break
                child = self.people[child.children[0]]
            if len(Available) == 0:
                return finalOrder
            if len(Available[0]) == 0:
                lastAvailable = Available[1:]
                return finalOrder
            for i in range(len(Available)):
                for x in Available[-i-1]:
                    finalOrder += recurseDown(x)
            return finalOrder
        order = [self.originatorName]
        for i in self.people[self.originatorName].children:
            order += recurseDown(i)
        return order
        
                
                    
        
            
            

    def get_seniority_order(self):
        """Returns the seniority succession order for Envoy of the Kiktil.

        Seniority order prioritizes proximity to the Originator, only moving on
        to a younger generation after every individual in the previous
        generations. Within a generation, older siblings come before younger,
        and cousins are prioritized by oldest different ancestor.

        Target Complexity: O(N), where N is how many indivduals have been added.

        Returns:
            A list of the names of individuals in seniority succession order
            starting with the Originator.
        """
        maxLevel = 0
        order, finalOrder = [[self.originatorName]], []
        for i in self.people:
            child = self.people[i]
            if child.level >= maxLevel:
                maxLevel += 1
                order.append([])
            order[child.level+1] += child.children
        
        for i in order:
            finalOrder += i
        return finalOrder
        
            
           
        

    def get_cousin_dist(self, lhs_name, rhs_name):
        """Determine the degree and removal of two cousins.

        The order of an individual relative to an ancestor is the number of
        generations separating them. So a child is order 0, a grandchild is
        order 1, and so on. For consistency, an individual has order -1 to
        themself.
        Consider the orders of two individuals relative to their most recent
        shared ancestor.
        The degree of the cousin relation of these individuals is the lesser of
        their orders.
        The removal of the cousin relation is the difference in their orders.

        Target Complexity: O(N), where N is how many indivduals have been added.
        

        Args:
            lhs_name: The name of one cousin.
            rhs_name: The name of the other cousin.

        Returns:
            A pair `(degree, removal)` of the degree and removal of the cousin
            relation between the specified individuals.
        """
        lhs, rhs = self.people[lhs_name], self.people[rhs_name]
        lhsParent, rhsParent = lhs, rhs
        lhsHistory, rhsHistory = [lhs_name], [rhs_name]
        shared = self.originatorName
        while lhsParent.parentName != None:
            lhsParent = self.people[lhsParent.parentName]
            lhsHistory.append(lhsParent.name)
        while rhsParent.parentName != None:
            rhsParent = self.people[rhsParent.parentName]
            rhsHistory.append(rhsParent.name)
        minLen = min(len(lhsHistory), len(rhsHistory))
        lenDiff = abs(len(rhsHistory)-len(lhsHistory))
        if minLen == len(lhsHistory):
            rhsHistory = rhsHistory[lenDiff:] 
        elif minLen == len(rhsHistory):
            lhsHistory = lhsHistory[lenDiff:]
        for i in range(len(rhsHistory)):
               if rhsHistory[i] == lhsHistory[i]:
                   shared = rhsHistory[i]
                   break
        sharedLevel = self.people[shared].level + 1
        lhsLevel, rhsLevel = lhs.level - sharedLevel, rhs.level - sharedLevel
        if shared == lhs_name:
            lhsLevel = -1
        elif shared == rhs_name:
            rhsLevel = -1
        return (min(lhsLevel, rhsLevel), abs(lhsLevel - rhsLevel))
                   
            
            
        
