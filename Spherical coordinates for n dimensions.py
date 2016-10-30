def list_transfer(listed):
    return_list = []
    for item in listed:
        return_list.append(item)
    return return_list

alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','z','x','y']

        
def find_dimensions(dimensions):
    basic = [[1],[0]]
    if dimensions > 2:
        for num in range(dimensions-2):
            temp = list_transfer(basic[0])
            basic.insert(0,temp)
            basic[0].append(1)
            basic[1].append(0)
            print(num)
    return basic


def dimensions_to_string(basic, codex):
    coord_dict = {}
    for coord_index in range(len(basic)):
        coord_dict[codex[ (1+coord_index) * -1]] = []
        for value_index in range(len(basic[coord_index])):
            if basic[coord_index][value_index] == 1:
                coord_dict[codex[(1+coord_index) * -1]].append('sin(%s)' % codex[value_index])
            if basic[coord_index][value_index] == 0:
                coord_dict[codex[(1+coord_index) * -1]].append('cos(%s)' % codex[value_index])

    return coord_dict

def dict_to_value(dicti):
    for variable in sorted(dicti):
        print(variable + ' = ', end = ''),
        for expression in dicti[variable]:
            print(expression + ' * ', end = ''),
        print(end = '\n')

basic = find_dimensions(4)

dicti = dimensions_to_string(basic, alphabet)

dict_to_value(dicti)



            


        
