#DFS path finding function
def dfs(tree, start, goal):
    stack = [(start, [start])]
    visited = set()
    while stack:
        current, path = stack.pop()
        if current in visited:
            continue
        visited.add(current)
        if current == goal:
            #If path found, return path
            return path
        for neighbor in tree.get(current, []):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor]))
    #If no path found, return empty list
    return []
