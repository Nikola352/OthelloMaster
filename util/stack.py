class Stack(object):
    def __init__(self, capacity: int):
        self._capacity = capacity
        self._data = [None] * capacity
        self._top = -1

    def push(self, item):
        if self.is_full():
            raise Exception("Stack is full")
        self._top += 1
        self._data[self._top] = item

    def top(self):
        if self.is_empty():
            raise Exception("Stack is empty")
        return self._data[self._top]
    
    def pop(self):
        item = self.top()
        self._top -= 1
        return item
    
    def clear(self):
        self._top = -1
    
    def is_empty(self):
        return self._top == -1
    
    def is_full(self):
        return self._top == self._capacity - 1
    
    def size(self):
        return self._top + 1