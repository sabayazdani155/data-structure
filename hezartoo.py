
def solve_maze(maze):
    n = len(maze)
    

    if maze[0][0] == 1 or maze[n-1][n-1] == 1:
        print("Path Not Found!")
        return None
    

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    stack = []
    visited = [[False] * n for _ in range(n)]
    
    
    stack.append(((0, 0), [(0, 0)]))
    visited[0][0] = True
    
    while stack:
        (x, y), path = stack.pop()         
        
        if (x, y) == (n-1, n-1):
            return path
            
    
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if (0 <= nx < n and 0 <= ny < n and         
                maze[nx][ny] == 0 and                    
                not visited[nx][ny]):                   
                
                visited[nx][ny] = True
                new_path = path + [(nx, ny)]
                stack.append(((nx, ny), new_path))
    
    print("Path Not Found!")
    return None








n = int(input("enter the (n)"))
maze = []
for _ in range(n):
    row = list(map(int, input().split()))
    maze.append(row)


path = solve_maze(maze)

if path:
    print("\n" + "="*50)
    print("Path Found:")
    for i, (x, y) in enumerate(path):
        if i > 0:
            print(" → ", end="")
        print(f"({x},{y})", end="")
    print("\n" + "="*50)
    


    print("\nMaze با مسیر مشخص شده (2 = مسیر):")
    for i in range(n):
        for j in range(n):
            if (i, j) in path:
                print("2", end=" ")
            else:
                print(maze[i][j], end=" ")
        print()