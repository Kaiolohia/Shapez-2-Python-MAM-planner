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
        if len(s1.shape) >= 6:
            return
        # Break crystals on top shape, triggers a recalculation on groups.
        for i in range(len(s2.shape)):
            for j in range(len(s2.shape[i])):
                if s2.shape[i][j].startswith("c"):
                    s2.shape[i][j] = "--"
        s2.update_groups_bfs()

        def calculate_collision_distances(s1, s2):
            # Returns a list of distances, one per group in s2
            distances = []
            for group2 in s2.groups:
                min_distance = len(s1.shape)
                for (x2, y2) in group2:
                    for group1 in s1.groups:
                        for (x1, y1) in group1:
                            if y2 == y1:
                                d = (x2 + len(s1.shape)) - x1 - 1
                                if min_distance > d:
                                    min_distance = d
                distances.append(min_distance)
            return distances

        dists = calculate_collision_distances(s1, s2)

        # If all distances are zero, just stack and trim as before
        if all(dist == 0 for dist in dists):
            if (len(s1.shape) + len(s2.shape)) >= 6:
                diff = (len(s1.shape) + len(s2.shape)) - 6
                for _ in range(diff):
                    s2.shape.pop()
            s1.shape = s1.shape + s2.shape
            return
        else:
            # Prepare a new shape for the result, starting with s1's current shape
            new_shape = [row[:] for row in s1.shape]

            # Drop all group nodes from s2 by their calculated distance
            for group_idx, group2 in enumerate(s2.groups):
                dist = dists[group_idx]
                for (x2, y2) in group2:
                    val = s2.shape[x2][y2]
                    if val != "--" and val != "P-":
                        target_x = x2 + len(s1.shape) - dist
                        # Ensure the new_shape has enough layers
                        while len(new_shape) <= target_x:
                            new_shape.append(["--"] * len(new_shape[0]))
                        # Place the group node at its new position
                        new_shape[target_x][y2] = val

            # Handle pins: they always fall unless supported from below
            for x2 in range(len(s2.shape)):
                for y2 in range(len(s2.shape[x2])):
                    if s2.shape[x2][y2] == "P-":
                        # Find the lowest empty spot in this column
                        drop_to = len(new_shape) - 1
                        while drop_to > 0 and new_shape[(drop_to-1)][y2] == "--":
                            drop_to -= 1
                        # Only place the pin if it's at the bottom or supported by a non-empty cell directly below
                        if new_shape[drop_to - 1][y2] != "--":
                            new_shape[drop_to][y2] = "P-"

            # Trim to max 6 layers (remove from the top if needed)
            while len(new_shape) > 6:
                new_shape.pop(0)

            s1.shape = new_shape
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
        roots = []

        def is_valid(x, y):
            # Ensure the position is within bounds and not visited
            if not (0 <= x < rows and 0 <= y < cols) or visited[x][y]:
                return False
            # Skip only empty spaces ("--"), pins ("P-")
            return self._shape[x][y] not in ["--", "P-"]

        def find_group(x, y):
            visited[x][y] = True
            node = TreeNode((x, y))
            children = []
            # Check below, left, and right for connected shapes
            for nx, ny in [
                (x + 1, y),  # Below
                (x, (y - 1) % cols),  # Left (wrap around)
                (x, (y + 1) % cols),  # Right (wrap around)
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

        # Start from the last layer and iterate backwards, collect all roots
        for i in range(rows - 1, -1, -1):
            for j in range(cols):
                if self._shape[i][j] not in ["--", "P-"] and not visited[i][j]:
                    roots.append(find_group(i, j))

        # Collapse all trees and combine the results
        all_coords = []
        for root in roots:
            group_coords = self.collapse_tree_to_list(root)
            # Remove duplicates and sort within each group
            group_coords = sorted(list(set(group_coords)), key=lambda coord: (coord[0], coord[1]))
            all_coords.append(group_coords)
        self._groups = all_coords

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