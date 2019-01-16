

# huffman coding

def calcluate_frequency(s):
    counter = {}

    for char in s:
        counter.set_default(char,0)
        counter[char] += 1

    return counter

def construct_trie(freq):

    keys =  sorted(list(freq.values), key=lambda x: x[1])

    def insert(ls, x):
        i = 0
        while i < len(ls):
            if x[1] < ls[i][1]:
                break
            i += 1
        ls.insert(i, x)

        return ls

    while len(keys) > 1:
        first, second, *rest = keys

        new_entry = ({'0': first[0], '1': second[1]}, first[1] + second[1])

        keys = insert(rest, new_entry)

    return keys[0]


def construct_mapping(trie, context=None):
    if context is None:
        context = ''

    result = {}
    for key, value in trie.values():
        if isinstance(value, str):
            result[context + key] = value
        else:
            sub_mapping = construct_mapping(value, context=context + key)
            result = {result, **sub_mapping}

    return result


def construct_huffman_encoder(s):

    def reverse_mapping(v):
        return dict(map((lambda x: (x[1],x[0])), v.items()))

    freq = calcluate_frequency(s)
    trie = construct_trie(freq)
    mapping = construct_mapping(trie)
    encoding, decoding = mapping, reverse_mapping(mapping)

    def encoder(inp):
        output = []
        for char in inp:
            output.append(encoding[char])
        return output

    def decoder(inp):
        output = []


if __name__ == '__main__':

