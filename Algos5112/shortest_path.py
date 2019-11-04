# TODO: Your name, Cornell NetID
# TODO: Your Partner's name, Cornell NetID

# Please see instructions.txt for the description of this problem.

def node_present (node, explored_nodes):
    for i in explored_nodes:
        if i[0] == node:
            return True
    return False

def shortest_path(graph, source, target):
    
    explored_nodes = [(source,0)]
    prev_node = {}
    
    init_neighbours = graph.get_neighbors(source)
    for x in init_neighbours:
        prev_node[x[0]] = source
    
    while not node_present(target, explored_nodes):
    
        nn = graph.get_neighbors(source)
        nn.sort(key=lambda tup:tup[1])
        
        for i in nn:
            if i not in explored_nodes:
                current_node = i 
                explored_nodes.append(current_node)
                break
    
        neighbors_current = graph.get_neighbors(current_node[0])
    
        for i in neighbors_current:
            if graph.has_edge(source, i[0]):    
                ew = 0
                for ew_pair in nn:
                    if ew_pair[0] == i[0]:
                        ew = ew_pair[1]
                        break
                    
                if (i[1] + current_node[1]) < ew:
                    graph.add_edge(source, i[0], i[1] + current_node[1])
                    prev_node[i[0]] = current_node[0]
            else:
                graph.add_edge(source, i[0], i[1] + current_node[1])
                prev_node[i[0]] = current_node[0]
                
    x = target
    path = [target]
    while x != source:
        x = prev_node[x]
        path.append(x)
        
    path = path[::-1]
    return (path, explored_nodes[-1][1])
            
                
     
    
    
  # `graph` is an object that provides a get_neighbors(node) method that returns
  # a list of (node, weight) edges. both of your graph implementations should be
  # valid inputs. you may assume that the input graph is connected, and that all
  # edges in the graph have positive edge weights.
  # 
  # `source` and `target` are both nodes in the input graph. you may assume that
  # at least one path exists from the source node to the target node.
  #
  # this method should return a tuple that looks like
  # ([`source`, ..., `target`], `length`), where the first element is a list of
  # nodes representing the shortest path from the source to the target (in
  # order) and the second element is the length of that path
  #
  # NOTE: Please see instructions.txt for additional information about the
  # return value of this method.

  # TODO: YOUR CODE HERE, delete the `raise NotImplementedError`line below once you finish writing your code

