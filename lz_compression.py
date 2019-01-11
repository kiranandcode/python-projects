
s = 'ababcbababaaaaaaa'

def construct_lz_compressor(initial_alphabet):
    mapping = dict(((x,i + 1) for i,x in enumerate(initial_alphabet)))

    def compressor(string : str) -> str:

        next_value = len(initial_alphabet) + 1
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
    mapping = dict(((i + 1, (None, x)) for i,x in enumerate(initial_alphabet)))


    def decompressor(string):

        inp = iter(string)
        output = []
        stack = []

        try:
            code = next(inp)
        except StopIteration:
            return []

        old_code = code
        output.append(mapping[code])
        fin_char = mapping[code]


        while True:
            code = next(inp)

            if code not in mapping:
                output.append(fin_char)
                old_code = code
                mapping[(old_code, fin_char)] = code
            else:
                pass


        return output





    return deconstructor, mapping
