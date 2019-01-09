
s = 'ababcbababaaaaaaa'

def construct_lz_compressor(initial_alphabet):
    mapping = dict(((x,i + 1) for i,x in enumerate(initial_alphabet)))
    next_value = len(initial_alphabet) + 1
    prefix_string = None

    def compressor(string : str) -> str:
        inp = iter(string)

        output = []
        try:
            prefix_string = next(inp)
        except ValueError:
            return ''

        for char in inp:
            k = char
            wk = prefix_string + k
            print('k = ', char)
            print('wk = ', wk)
            if wk in mapping:
                print('wk in mapping')
                prefix_string = prefix_string + k
                print('w = ', prefix_string)
                continue
            else:
                print('wk not in mapping')
                output.append(mapping[prefix_string])
                mapping[wk] = next_value
                prefix_string = k
                print('w = ', prefix_string)
            print('output is ', output)

        if prefix_string is not None:
            output.append(mapping[prefix_string])
            return output

    return compressor, mapping
