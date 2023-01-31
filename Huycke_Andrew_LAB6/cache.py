import random
class cache:
    def __init__(self, cache_size, block_size, associativity, replacement):
        self.hits=0
        self.misses=0
        self.cache_size=cache_size
        self.block_size=block_size
        self.replacement=replacement
        num_sets = int(cache_size/block_size/associativity)
        self.num_sets=num_sets
        self.set_size=associativity
        self.table = []
        self.recently_used = [[] for i in range(num_sets)]
        for i in range(num_sets):
            self.table.append(['' for i in range(associativity)])

    def __str__(self):
        return f"{self.table}"

    def checkHit(self, trace):
        index = int(trace)%self.num_sets
        setToCheck = self.table[index]
        if trace in setToCheck:
            self.hits+=1
            #update recently used list, put trace at the front
            traceIndex=self.recently_used[index].index(trace)
            self.recently_used[index].pop(traceIndex)
            self.recently_used[index].insert(0, trace)
        else:
            self.misses+=1
            if self.set_size != 1:
                self.insert(trace)
            else:
                self.table[index][0]=trace
                #again, consider recently used list because of poor structure
                self.recently_used[index].insert(0, trace)
                #only take first element
                self.recently_used[index]=self.recently_used[index][0:1]

    def insert(self, trace):
        index = int(trace)%self.num_sets
        if '' in self.table[index]:
            #put trace in the next available empty spot
            replaceIndex=self.table[index].index('')
            self.table[index][replaceIndex]=trace
            #add trace to the beginning of the recently used list
            self.recently_used[index].insert(0, trace)
        elif self.replacement == "Random":
            indexToInsert = random.randint(0, self.set_size-1)
            valToRemove = self.table[index][indexToInsert]
            indexToRemove = self.recently_used[index].index(valToRemove)
            self.table[index][indexToInsert]=trace
            #have to update recency list so we don't get errors, I should fix the structure later
            self.recently_used[index].pop(indexToRemove)
            self.recently_used[index].insert(0,trace)
        elif self.replacement == "NMRU+Random":
            #can remove any element but the first
            indexToRemove = random.randint(1, self.set_size-1)
            valToRemove = self.recently_used[index][indexToRemove]
            indexToInsert = self.table[index].index(valToRemove)
            self.table[index][indexToInsert]=trace
            #update recently used list
            self.recently_used[index].pop(indexToRemove)
            self.recently_used[index].insert(0,trace)
        elif self.replacement == "LRU":
            #can only remove last element in recently used list
            valToRemove = self.recently_used[index][-1]
            indexToInsert = self.table[index].index(valToRemove)
            self.table[index][indexToInsert]=trace
            #update recently used list
            self.recently_used[index].pop(-1)
            self.recently_used[index].insert(0,trace)

    def print_output(self):
        print('\n')
        print(f'Cache_Size: {(self.cache_size/1000):.2f} KB')
        print(f'Block_Size: {self.block_size} words ({self.block_size*4} bytes)')
        print(f'Associativity: {self.set_size} way')
        print(f'Replacement_Policy: {self.replacement}')
        print(f'Total_Number_of_Accesses: {self.hits+self.misses}')
        print(f'Cache_Hits: {self.hits}')
        print(f'Cache_Misses: {self.misses}')
        print(f'Cache_Hit_Rate: {(100*self.hits/(self.hits+self.misses)):.2f}%')
        print(f'Cache_Miss_Rate: {(100*self.misses/(self.hits+self.misses)):.2f}%')