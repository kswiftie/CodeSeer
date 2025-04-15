def updateMatrix(self, matrix: list[list[int]]) -> list[list[int]]:
    rows = len(matrix)
    if rows == 0:
        return []

    cols = len(matrix[0])
    mx = rows * cols
    dis = [[mx for _ in range(cols)] for _ in range(rows)]

    for i in range(rows - 1, -1, -1):
        for j in range(cols - 1, -1, -1):
            if matrix[i][j] == 0:
                dis[i][j] = 0
            else:
                right = dis[i][j + 1] if j + 1 < cols else mx
                down = dis[i + 1][j] if i + 1 < rows else mx
                dis[i][j] = 1 + min(right, down)

    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == 0:
                dis[i][j] = 0
            else:
                left = dis[i][j - 1] if j - 1 >= 0 else mx
                top = dis[i - 1][j] if i - 1 >= 0 else mx
                dis[i][j] = min(dis[i][j], 1 + min(left, top))  # pay attention here

    return dis