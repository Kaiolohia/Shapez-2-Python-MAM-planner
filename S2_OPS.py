#TreeNode class for finding groups in a shape
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.below = None  # New child for connections between layers
# Machines class encapsulates the operations on shapes
class machines:
    # Mimic the behavior of stacking shapes found in Shapez 2
    def stack(s1, s2):
        if len(s1.shape) >= 6:
            return
        # Break crystals on top shape, triggers a recalculation on groups.
        for i in range(len(s2.shape)):
            for j in range(len(s2.shape[i])):
                if s2.shape[i][j].startswith("c"):
                    s2.shape[i][j] = "--"
        s2.update_groups_bfs()
        
        # Prepare a new shape for the result, starting with s1's current shape
        new_shape = [row[:] for row in s1.shape] + [["--"] * len(s1.shape[0]) for _ in range(len(s2.shape))]

        # Drop all group nodes from s2 by their calculated distance
        for group in s2.groups:
            # Find the max drop for this group
            max_drop = 0
            while True:
                can_drop = True
                for (x2, y2) in group:
                    val = s2.shape[x2][y2]
                    if val == "--":
                        continue
                    target_x = x2 + len(s1.shape) + max_drop
                    # Check if we are at the bottom or if the cell below is occupied
                    if target_x == 0 or new_shape[target_x - 1][y2] != "--":
                        can_drop = False
                        break
                if can_drop:
                    max_drop -= 1
                else:
                    break

            # Place the group at the lowest possible position
            for (x2, y2) in group:
                val = s2.shape[x2][y2]
                if val != "--":
                    target_x = x2 + len(s1.shape) + max_drop
                    new_shape[target_x][y2] = val

        # Trim to max 6 layers (remove from the top if needed)
        while len(new_shape) > 6:
            new_shape.pop()

        s1.shape = new_shape
        return
    # Mimic the behavior of painting shapes found in Shapez 2
    def paint(s1, color):
        for j in range(len(s1.shape[-1])):
            if s1.shape[-1][j] != "P-" and not "c" in s1.shape[-1][j][0] and s1.shape[-1][j] != "--":
                s1.shape[-1][j] = s1.shape[-1][j][0] + color
        return
    # Mimic the behavior of generating crystals found in Shapez 2
    def gen_crystal(s1, color):
        for i in range(len(s1.shape)):
            for j in range(len(s1.shape[i])):
                if s1.shape[i][j] == "--" or s1.shape[i][j] == "P-":
                    s1.shape[i][j] = f"c{color}"
    # Mimic the behavior of swapping two shapes found in Shapez 2
    def swap(s1, s2):
        # return true if s1 layers are less or equal to s2 layers
        if len(s1.shape) <= len(s2.shape):
            for i in range(len(s1.shape)):
                new_shape_1 = s1.shape[i][0:3] + s2.shape[i][3:]
                new_shape_2 = s2.shape[i][0:3] + s1.shape[i][3:]
                s1.shape[i] = new_shape_1
                s2.shape[i] = new_shape_2
            for i in range(len(s2.shape) - len(s1.shape)):
                s1.shape.append(["--", "--", "--"] + s2.shape[i][3:])
            return
        else:
            for i in range(len(s2.shape)):
                new_shape_1 = s2.shape[i][0:3] + s1.shape[i][3:]
                new_shape_2 = s1.shape[i][0:3] + s2.shape[i][3:]
                s1.shape[i] = new_shape_1
                s2.shape[i] = new_shape_2
            for i in range(len(s1.shape) - len(s2.shape)):
                s2.shape.append(["--", "--", "--"] + s1.shape[len(s2.shape) + i][3:])
            return

    def rotate_cw(s1):
        # Rotate the shape clockwise by moving the last index to the first index
        for i in range(len(s1.shape)):
            s1.shape[i] = [s1.shape[i][-1]] + s1.shape[i][:-1]
        return

    def rotate_ccw(s1):
        # Rotate the shape counter-clockwise by moving the first index to the last index
        for i in range(len(s1.shape)):
            s1.shape[i] = s1.shape[i][1:] + [s1.shape[i][0]]
        return
    def rotate_180(s1):
        # Rotate the shape 180 degrees by moving the last index to the front 3 times
        for i in range(len(s1.shape)):
            for _ in range(3):  # Repeat the operation 3 times
                s1.shape[i] = [s1.shape[i][-1]] + s1.shape[i][:-1]
        return
        
    def pin(s1):
        blank = shape("------------")
        for i in range(len(s1.shape[0])):
            if s1.shape[0][i] != "--":
                blank.shape[0][i] = "P-"
        if len(s1.shape) == 6:
            s1.shape.pop()
            s1.shape.insert(0, blank.shape[0])
        else:
            s1.shape.insert(0, blank.shape[0])
# Shape class holds data relating to shapes and computes groups on shape creation
class shape:
    def __init__(self, shape_code: str):
        self._shape = self.decode_shape(shape_code)
        self._groups = []
        self.update_groups_bfs()

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, value):
        self._shape = value

    @property
    def groups(self):
        return self._groups

    # Creates a matrix of found group coordinates
    def collapse_tree_to_list(self, node):
        if node is None:
            return []
        
        # Collect the current node's value and recursively collect from children
        result = [node.value]
        result += self.collapse_tree_to_list(node.left)
        result += self.collapse_tree_to_list(node.right)
        result += self.collapse_tree_to_list(node.below)
        
        # Sort the list first by x (row) and then by y (column)
        return sorted(result, key=lambda coord: (coord[0], coord[1]))

    # Using BFS, find all groups stemming from the top layer
    def update_groups_bfs(self):
        rows = len(self._shape)
        cols = len(self._shape[0])
        visited = [[False for _ in range(cols)] for _ in range(rows)]
        all_groups = []

        def is_valid(x, y):
            # Ensure the position is within bounds and not visited
            if not (0 <= x < rows and 0 <= y < cols) or visited[x][y]:
                return False
            # Skip only empty spaces ("--"), pins ("P-")
            return self._shape[x][y] not in ["--", "P-"]

        def find_group(x, y):
            # BFS for a group within a single layer
            queue = [(x, y)]
            group = []
            visited[x][y] = True
            while queue:
                cx, cy = queue.pop(0)
                group.append((cx, cy))
                # Check left and right (with wraparound)
                for ny in [(cy - 1) % cols, (cy + 1) % cols]:
                    if is_valid(cx, ny):
                        visited[cx][ny] = True
                        queue.append((cx, ny))
            return group

        # Only check for groups within each layer
        for i in range(rows):
            for j in range(cols):
                if self._shape[i][j] == "P-" and not visited[i][j]:
                    all_groups.append([(i, j)])
                    visited[i][j] = True
                elif is_valid(i, j):
                    group = find_group(i, j)
                    if group:
                        # Sort each group by x, then y (though x is constant here)
                        group = sorted(group, key=lambda coord: (coord[0], coord[1]))
                        all_groups.append(group)
        self._groups = all_groups

    # Converts shape code into a matrix
    def decode_shape(self, shape_code: str):
        s = []
        if ":" in shape_code:
            layers = shape_code.split(':')
        else:
            layers = [shape_code]
        for f in layers:
            layer = [f[i:i + 2] for i in range(0, len(f), 2)]
            s.append(layer)
        return s

    def __str__(self):
        # Converts shape matrix into shape code
        return ':'.join([''.join(layer) for layer in self.shape])


s1 = shape("P-----------")
s2 = shape("HuHu--------:--HuHu------:----HuHu----:------HuHu--:--------HuHu")
machines.stack(s1, s2)
print(s1)