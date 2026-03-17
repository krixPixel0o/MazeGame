import heapq
from collections import deque

def get_valid_neighbors(maze, x, y):
   
    neighbors = []
    cell = maze.grid[x][y]
    
    if not cell.walls['top'] and y > 0:
        neighbors.append((x, y - 1))
    if not cell.walls['right'] and x < maze.cols - 1:
        neighbors.append((x + 1, y))
    if not cell.walls['bottom'] and y < maze.rows - 1:
        neighbors.append((x, y + 1))
    if not cell.walls['left'] and x > 0:
        neighbors.append((x - 1, y))
        
    return neighbors

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from and came_from[current] is not None:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def dfs(maze, start_pos, end_pos):
    
    stack = [start_pos]
    came_from = {start_pos: None}
    visited = set([start_pos])
    
    while stack:
        current = stack.pop()
        
        if current == end_pos:
            return reconstruct_path(came_from, current)
            
        for neighbor in get_valid_neighbors(maze, current[0], current[1]):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                stack.append(neighbor)
                
    return None # No path found

def bfs(maze, start_pos, end_pos):
   
    queue = deque([start_pos])
    came_from = {start_pos: None}
    visited = set([start_pos])

    while queue:
        current = queue.popleft()
        
        if current == end_pos:
            return reconstruct_path(came_from, current)
            
        for neighbor in get_valid_neighbors(maze, current[0], current[1]):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)
                
    return None

def dijkstra(maze, start_pos, end_pos):
    
    # Uses a priority queue storing (cost, (x, y))
    pq = [(0, start_pos)]
    came_from = {start_pos: None}
    cost_so_far = {start_pos: 0}
    visited = set()
    
    while pq:
        current_cost, current = heapq.heappop(pq)
        
        if current == end_pos:
            return reconstruct_path(came_from, current)
            
        if current in visited:
            continue
        visited.add(current)
            
        for neighbor in get_valid_neighbors(maze, current[0], current[1]):
            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current
                heapq.heappush(pq, (new_cost, neighbor))
                
    return None

def a_star(maze, start_pos, end_pos):
   
    def heuristic(a, b):
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
    pq = [(0, start_pos)]
    came_from = {start_pos: None}
    cost_so_far = {start_pos: 0}
    visited = set()
    
    while pq:
        _, current = heapq.heappop(pq)
        
        if current == end_pos:
            return reconstruct_path(came_from, current)
            
        if current in visited:
            continue
        visited.add(current)
            
        for neighbor in get_valid_neighbors(maze, current[0], current[1]):
            new_cost = cost_so_far[current] + 1
            
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(end_pos, neighbor)
                came_from[neighbor] = current
                heapq.heappush(pq, (priority, neighbor))
                
    return None
