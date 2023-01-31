import csv
from cache import cache

#get ooptions to later configure the cache
def get_user_input(cache_sizes, block_sizes, associativities, replacements):
    for i in range(0, len(cache_sizes)):
        print(f'{i+1}. {2**(i+4)} KiB')
    cache_size=cache_sizes[int(input("pick a cache size (1-5): "))-1]

    for i in range(0, len(block_sizes)):
        print(f'{i+1}. {block_sizes[i]} words')
    block_size=block_sizes[int(input("pick a block size (1-3): "))-1]

    for i in range(0, len(associativities)):
        print(f'{i+1}. {associativities[i]}')
    associativity=associativities[int(input("pick an associativity (1-5): "))-1]

    for i in range(0, len(replacements)):
        print(f'{i+1}. {replacements[i]}')
    replacement=replacements[int(input("pick a replacement method (1-3): "))-1]

    return [cache_size, block_size, associativity, replacement]

#puts all trace values into a list
def parse_tracefile(filename):
    word_list=[]
    with open(filename) as f:
        for row in f:
            trace = row.strip()
            word_list.append(trace)
    return word_list

cache_sizes = [2**(14+i) for i in range(5)] #We want to operate in powers of 2
cache_decimal_sizes = [2**(4+i) for i in range(5)] #The user will see the KiB values instead of Bytes
block_sizes = [2, 4, 8]
associativities = [2**i for i in range(5)]
replacements = ['LRU', 'Random', 'NMRU+Random']

options_picked = get_user_input(cache_sizes, block_sizes, associativities, replacements)

cache_size = int(options_picked[0])
block_size = int(options_picked[1])
associativity = int(options_picked[2])
replacement = options_picked[3]

test = cache(cache_size, block_size, associativity, replacement)

#below code was used to put all possible cache configuration performances in a csv file
"""
traces = parse_tracefile("tracefile.txt")

with open('cache_performance.csv','w', encoding='UTF8', newline='') as f:
    writer=csv.writer(f)
    header = ['Cache_Size', 'Block_Size', 'Associativity', 'Replacement_Policy', 'Cache_Hit_Rate']
    writer.writerow(header)

    for cache_size in cache_sizes:
        for block_size in block_sizes:
            for associativity in associativities:
                for replacement in replacements:
                    test = cache(cache_size, block_size, associativity, replacement)
                    for trace in traces:
                        test.checkHit(trace)
                    hit_rate = f"{(test.hits/(test.hits+test.misses)):.4f}"
                    writer.writerow([cache_decimal_sizes[cache_sizes.index(cache_size)], test.block_size, test.set_size, test.replacement, hit_rate])
"""

traces = parse_tracefile("tracefile.txt")
for trace in traces:
    test.checkHit(trace)  

test.print_output()