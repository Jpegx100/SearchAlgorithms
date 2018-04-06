def copy_matrix(matrix):
    return [m.copy() for m in matrix]

def print_tree(node):
    if node:
        if node.father:
            print_tree(node.father)
        print(node.content)

def node_in_states(node, states):
    for state in states:
        if state.content == node.content:
            return True
    return False

def print_states(states, show_attrs=False, show_tab=True):
    if show_attrs:
        for state in states:
            print('  H = '+str(state.heuristic_value), end='     ')
        print('')
    
    if show_tab:
        if len(states)>0:
            for i in range(len(states[0].content)):
                for state in states:
                    end = '   '
                    print(state.content[i], end=end)
                print('')