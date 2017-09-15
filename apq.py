#-----------------------------------------------------------------------------
# Adaptable Priority Queue ---------------------------------------------------
#-----------------------------------------------------------------------------

class Element:

    """A key, value, and index"""

    def __init__(self, k, v, i):
        self._key = k
        self._value = v
        self._index = i

    def __eq__(self, other):
        return self._key == other._key

    def __lt__(self, other):
        return self._key < other._key

    def _wipe(self):
        self._key = None
        self._value = None
        self._index = None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str((self._key, self._value))


class APQ:

    """Does what it says on the tin"""

    def __init__(self):
        self._body = []
        self._length = 0

    def add(self, key, item):
        #Add a new item into APQ with priority key, and return
        #its Element in the APQ
        element = Element(key, item, self._length)
        self._body.append(element)
        self._length += 1
        self._rebalance(element._index)
        return element

    def min(self):
        return self._body[0]

    def remove_min(self):
        #Remove and return the value with the minimum key
        element = self._body[0]
        self._length -= 1
        if self._length > 0:
            last = self._body.pop()
            self._body[0] = last
            self._rebalance(0)
        else:
            self._body.pop()
        element._index = None
        return element

    def is_empty(self):
        #Return True if no items in APQ
        if self._length == 0:
            return True
        else:
            return False

    def length(self):
        return self._length

    def update_key(self, element, newkey):
        #Update the key in element to be newkey, rebalance APQ
        element._key = newkey
        self._rebalance(element._index)

    def get_key(self, element):
        return element._key

    def remove(self, element):
        self._body[element._index] = self._body.pop()
        self._length -= 1
        self._rebalance(element._index)
        element._index = None
        return element

    def _rebalance(self, index):
        #Rebalance APQ, checking from index onwards
        while index < self._length:
            if index > 0:
                #If the element's key is less than its parent's key, swap places
                if self._body[index] < self._body[(index-1)//2]:
                    self._body[(index-1)//2], self._body[index] = self._body[index], self._body[(index-1)//2]
                    #Swap the indices of the two elements
                    self._body[(index-1)//2]._index, self._body[index]._index = self._body[index]._index, self._body[(index-1)//2]._index
                    index = (index-1)//2
                    continue
            #If the element's key is greater than its left child's, swap places    
            if (2*index)+1 < self._length and self._body[index] > self._body[(2*index)+1]:
                self._body[index], self._body[2*index+1] = self._body[2*index+1], self._body[index]
                #Swap the indices
                self._body[index]._index, self._body[2*index+1]._index = self._body[2*index+1]._index, self._body[index]._index
                index = (2*index)+1
                continue
            #If the element's key is greater than its right child's, swap places
            elif (2*index)+2 < self._length and self._body[index] > self._body[(2*index)+2]:
                self._body[index], self._body[2*index+2] = self._body[2*index+2], self._body[index]
                #Swap the indices
                self._body[index]._index, self._body[2*index+2]._index = self._body[2*index+2]._index, self._body[index]._index
                index = (2*index)+2
                continue
            else:
                break

    def __str__(self):
        return str(self._body)
