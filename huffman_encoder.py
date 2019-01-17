

# huffman coding

def calcluate_frequency(s):
    counter = {}

    for char in s:
        counter.setdefault(char,0)
        counter[char] += 1

    return counter

def construct_trie(freq):

    keys =  sorted(list(freq.items()), key=lambda x: x[1])

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

        new_entry = ({'0': first[0], '1': second[0]}, first[1] + second[1])

        keys = insert(rest, new_entry)

    return keys[0][0]


def construct_forward_mapping(trie, context=None):
    if context is None:
        context = ''

    result = {}
    for key, value in trie.items():
        if isinstance(value, str):
            result[value] = context + key
        else:
            sub_mapping = construct_forward_mapping(value, context=context + key)
            result = {**result, **sub_mapping}

    return result


def construct_huffman_encoder(s,
                              raise_missing=False):

    freq = calcluate_frequency(s)
    trie = construct_trie(freq)
    mapping = construct_forward_mapping(trie)

    def encoder(inp):
        output = []
        for char in inp:

            if not char in mapping and raise_missing:
                raise ValueError('character {char} not in initial mapping')
            elif not char in mapping:
                output.append(char)
            else:
                output.append(mapping[char])

        return ''.join(output)

    def decoder(inp):
        output = []

        trie_ref = trie
        current_prefix_string = []

        for value in inp:

            # if we see a value in trie_ref
            if value in trie_ref:
                # update trie ref
                trie_ref = trie_ref[value]

                # if trie_ref has reached a leaf value - output it
                if isinstance(trie_ref, str):
                    output.append(trie_ref)
                    # also reset the trie to the start and
                    # empty the prefix string
                    trie_ref = trie
                    current_prefix_string = []
                else:
                    # otherwise extend the current prefix string
                    current_prefix_string.append(value)
            else:
                # which means we found a character we don't know about
                if raise_missing:
                    raise ValueError('character {value} not in initial mapping')
                else:
                    # if we're being leniant, just output the prefix string and
                    # the next character
                    output.extend(current_prefix_string)
                    output.append(value)
                    # reset the trie to the start and empty the prefix string
                    trie_ref = trie
                    current_prefix_string = []

        return ''.join(output)

    return encoder, decoder


if __name__ == '__main__':
    print('Huffman encoder Implementation')

    test_string = 'This is an example string that one might want to compress into a smaller format for transferring over the internet or other such means. This conversion program will convert this string into a huffman encoding and thereby reduce the cost of transferring this document.'

    print(f'Input string length: {len(test_string) * 8}')
    print(f'Input string sample: {test_string[:30]}')

    print(f'Constructing compressor')

    encoder, decoder = construct_huffman_encoder(test_string)

    print(f'Constructed compressor')

    compressed_string = encoder(test_string)

    print(f'Compressed string length: {len(compressed_string)}')
    print(f'Compressed string sample: {compressed_string[:30]}')

    decompressed_string = decoder(compressed_string)

    print(f'Decompressed string matches: {decompressed_string == test_string}')

    while True:
        text = input('\n>>> Enter some text to be compressed:')
        compressed = encoder(text)
        decompressed = decoder(compressed)
        print(f'Input: {text}')

        print(f'Input length: {len(text) * 8}')

        print(f'Compressed: {compressed}')
        print(f'Compressed length: {len(compressed)}')

        print(f'Decompressed: {decompressed}')
        print(f'Decompression success: {decompressed == text}')

