
s = 'ababcbababaaaaaaa'

def construct_lz_compressor(initial_alphabet):
    mapping = dict(((x,i + 1) for i,x in enumerate(initial_alphabet)))
    next_value = len(initial_alphabet) + 1

    def compressor(string : str) -> str:

        nonlocal mapping
        nonlocal next_value

        prefix_string = None
        inp = iter(string)

        output = []
        try:
            prefix_string = next(inp)
        except StopIteration:
            return []

        for char in inp:

            k = char
            wk = prefix_string + k

            # print('===========================================')
            # print('k = ', char)
            # print('wk = ', wk)

            if wk in mapping:
                # print('wk in mapping')

                # print('w: {} -> {}'.format(prefix_string, prefix_string + k))

                prefix_string = prefix_string + k
                continue
            else:
                # print('wk not in mapping')
                # print('w: {} -> {}'.format(prefix_string, k))

                value = next_value
                next_value += 1

                # print('appending mapping[{}] = {}'.format(prefix_string, mapping[prefix_string]))
                # print('adding mapping[{}] = {}'.format(wk, value))

                output.append(mapping[prefix_string])

                mapping[wk] = value

                prefix_string = k

            # print('output is ', output)

            # print('===========================================\n\n')

        if prefix_string is not None:
            output.append(mapping[prefix_string])
            return output

    return compressor, mapping


def construct_lz_decompressor(initial_alphabet):
    mapping = dict((i + 1,  x) for i,x in enumerate(initial_alphabet))
    next_code = len(initial_alphabet) + 1


    def decompressor(string):
        nonlocal next_code
        nonlocal mapping

        inp = iter(string)
        output = []

        try:
            prev_code = next(inp)
        except StopIteration:
            return []

        prev_word = mapping[prev_code]
        output.append(prev_word)


        for code in inp:
            if code in mapping:
                word = mapping[code]
                prev_word = mapping[prev_code]
                new_word = prev_word + word[0]

                # insert new word into mapping
                mapping[next_code] = new_word
                next_code += 1

                output.append(word)
            else:
                prev_word = mapping[prev_code]
                new_word = prev_word + prev_word[0]

                # insert new word into mapping
                mapping[next_code] = new_word
                next_code += 1

                output.append(new_word)

            prev_code = code

        return output



    return decompressor, mapping


def run_example():
    input_alphabet = ['a','b','c']
    compressor, cmap = construct_lz_compressor(input_alphabet)
    decompressor, dmap = construct_lz_decompressor(input_alphabet)

    print("String: {}".format(s))
    compressed = compressor(s)
    print("compressed: {}".format(compressed))
    print("cmap: {}".format(str(cmap)))

    decompressed = ''.join(decompressor(compressed))

    print("decompressed: {}".format(decompressed))
    print("dmap: {}".format(str(dmap)))

    print('decompressed == s : {}'.format(decompressed == s))


if __name__ == '__main__':
    run_example()
