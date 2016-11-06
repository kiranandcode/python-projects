import math
operations = [0b1100100000000000, 0b1110010000000000, 0b0111001000000000, 0b0011000100000000, 0b1000110010000000,
              0b0100111001000000, 0b0010011100100000, 0b0001001100010000, 0b0000100011001000, 0b0000010011100100,
              0b0000001001110010, 0b0000000100110001, 0b0000000010001100, 0b0000000001001110, 0b0000000000100111,
              0b0000000000010011]


class Node:
    def __init__(self, state=int, status=int):
        self.state = state
        self.status = status


dumbo = {0: 13, 1: 14, 2: 15, 3: 16, 4: 9, 5: 10, 6: 11, 7: 12, 8: 5, 9: 6, 10: 7, 11: 8, 12: 1, 13: 2, 14: 3, 15: 4}


def state_status(value):
    count = 0;
    while value !=0:
        count += 1
        value &= value-1
    return count


N = []
T = []
cost = {}
steps = {}
prev = {}
change_operator = {}

def check_compatible(operator, state):
    if (state >> len(operations)-operations.index(operator)-1) & 1 == 1:
        return True
    else:
        return False


def find_lowest_cost_node():
    global T
    global N
    minimum = math.inf
    for node in N:
        if node not in T:
            if cost[node] < minimum:
                minimum = cost[node]
                temp = node
    return temp


def update_node_costs(node = Node):
    global steps
    global cost
    global N
    global prev
    global change_operator
    for operator in operations:
        # updates costs of existing nodes accessible via new one, or adds cost of new nodes

        if check_compatible(operator, node.state):
            new_node = Node(node.state ^ operator, state_status(node.state ^ operator))
            if new_node in cost:
                if cost[new_node] > state_status(new_node.state) + (steps[node] + 1)/1:
                    cost[new_node] = state_status(new_node.state) + (steps[node] + 1)/1
                    steps[new_node] = steps[node] + 1
                    prev[new_node] = node
                    change_operator[new_node] = operator
            else:
                cost[new_node] = state_status(new_node.state) + (steps[node] + 1)/1
                steps[new_node] = steps[node] + 1
                prev[new_node] = node
                change_operator[new_node] = operator

            # adds new nodes to N
            if new_node not in N:
                N.append(new_node)

    # find lowest path cost = step+cost - in set of nodes that are not in T
    # update costs of all nodes using newly added node, generating nodes, updating queries ifnecassary


def djiksta(start = int):
    global change_operator
    global prev
    global N
    global T
    start_node = Node(start, state_status(start))
    N.append(start_node)
    T.append(start_node)
    # generates initial nodes for searching
    for operator in operations:
        if check_compatible(operator, start_node.state):
            N.append(Node(start_node.state ^ operator, state_status(start_node.state ^ operator)))
            steps[N[-1]] = 1
            cost[N[-1]] = 1 + N[-1].status
            prev[N[-1]] = start_node
            change_operator[N[-1]] = operator
    current = find_lowest_cost_node()


    while state_status(current.state) != 0:
        current = find_lowest_cost_node()
        T.append(current)
        update_node_costs(current)
    return current


def printPath():
    global change_operator
    global prev
    output = []


    for i, v in change_operator.items():
        #print(i.status, ":", i)
        if i.status == 0:
            current = i

    while current != N[0]:
        output.append(change_operator[current])
        current = prev[current]

    output.reverse()


    for i in output:
        print(dumbo[operations.index(i)])

def gen_input(*args):
    output = []
    for i in range(16):
        if dumbo[i] in args:
            output.append(1)
        else:
            output.append(0)

    binary = "".join(map(str, output))
    return int(binary, base=2)



end = djiksta(gen_input(1, 4, 6, 9, 10, 12, 13, 16))

printPath()

#print(check_compatible(operations[6],0b1000000100000000))





