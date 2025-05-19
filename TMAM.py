# Step 1, Input ✅
# Step 2, layer break down ✅
# Step 3, Section building 
# Step 4, Stack respective sections
# Step 5, Now that we have 6 shapes each representing one section per shape, we need to swap parts around to build our final shape. 

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.below = None  # New child for connections between layers

class machines:
    def stack(s1, s2):
        # Break crystals on top shape, triggers a recalculation on groups.
        for i in range(len(s2.shape)):
            for j in range(len(s2.shape[i])):
                if s2.shape[i][j].startswith("c"):
                    s2.shape[i][j] = "--"
        
        def calculate_collison_distance(s1, s2):
            distance = 5
            for i in range (len(s2.groups)):
                if distance == 1:
                    return 1
                x2 = s2.groups[i][0] + len(s1.shape)
                y2 = s2.groups[i][1]
                for j in range(len(s1.groups)-1, -1, -1):
                    if distance == 1:
                        return 1
                    x1 = s1.groups[j][0]
                    y1 = s1.groups[j][1]
                    if y2 == y1:            
                        if distance >= x2 - x1:
                            distance = x2 - x1
            return distance
        dist = calculate_collison_distance(s1, s2)
        if dist == 1:
            s1.shape = s1.shape + s2.shape
            return
        else:
            return

                    
        
    def paint(s1, color):
        for j in range(len(s1.shape[-1])):
            if s1.shape[-1][j] != "P-" and not "c" in s1.shape[-1][j][0] and s1.shape[-1][j] != "--":
                s1.shape[-1][j] = s1.shape[-1][j][0] + color
        return
    
    def gen_crystal(s1, color):
        for i in range(len(s1.shape)):
            for j in range(len(s1.shape[i])):
                if s1.shape[i][j] == "--" or s1.shape[i][j] == "P-":
                    s1.shape[i][j] = f"c{color}"
    
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

class shape:
    def __init__(self, shape_code: str):
        self._shape = self.decode_shape(shape_code)
        self._groups = self.update_groups_bfs()

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, value):
        self._shape = value
        self._groups = self.update_groups_bfs()

    @property
    def groups(self):
        return self._groups

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

    def update_groups_bfs(self):
        rows = len(self._shape)
        cols = len(self._shape[0])
        visited = [[False for _ in range(cols)] for _ in range(rows)]
        root = None

        def is_valid(x, y):
            # Ensure the position is within bounds and not visited
            if not (0 <= x < rows and 0 <= y < cols) or visited[x][y]:
                return False

            # Allow nodes below to be added even if they are part of the same group
            # Skip only empty spaces ("--"), pins ("P-"), or crystals ("c")
            return self._shape[x][y] not in ["--", "P-"]

        def find_group(x, y):
            visited[x][y] = True
            node = TreeNode((x, y))
            children = []

            # Check below, left, and right for connected shapes
            for nx, ny in [
                (x + 1, y),  # Below
                (x, (y - 1) % cols),  # Left (wrap around to the last index if y == 0)
                (x, (y + 1) % cols),  # Right (wrap around to the first index if y == cols - 1)
            ]:
                if is_valid(nx, ny):
                    child_node = find_group(nx, ny)
                    children.append(child_node)

            # Assign children to the binary tree
            if len(children) > 0:
                node.left = children[0]
            if len(children) > 1:
                node.right = children[1]

            # Check directly below for connections between layers
            if x - 1 < rows and is_valid(x - 1, y):
                node.below = find_group(x - 1, y)

            return node

        # Start from the last layer and iterate backwards
        for i in range(rows - 1, -1, -1):  # Iterate from the last layer to the first
            for j in range(cols):
                if self._shape[i][j] not in ["--", "P-"] and not visited[i][j]:
                    if root is None:
                        root = find_group(i, j)  # Set the first group as the root
                    else:
                        find_group(i, j)  # Continue finding other groups
        return self.collapse_tree_to_list(root)

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
        # Flatten the nested lists and concatenate the string pairs
        return ':'.join([''.join(layer) for layer in self.shape])

s1 = shape('HuP-ccFucmGm:GbGucrP-GyP-:HuP-P-P-cyHy:HbGgGrFucmGk:HuFyFc------')
s2 = shape("------crGbP-")
s3 = shape("FgGuGcP-HwFk")
machines.stack(s1, s2)
print(s1)