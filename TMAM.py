# Step 1, Input ✅
# Step 2, layer break down ✅
# Step 3, Section building 
# Step 4, Stack respective sections
# Step 5, Now that we have 6 shapes each representing one section per shape, we need to swap parts around to build our final shape. 

class machines:
    def stack(s1, s2):
        # check if top layer combines with bottom layer
         # Break crystals when dropped
        for i in range(len(s2.shape)):
            for j in range(len(s2.shape[i])):
                if s2.shape[i][j][0] == "c":
                    s2.shape[i][j] = "--"
        if all((b == "--" or (a == "--" and b != "--")) for a, b in zip(s1.shape[-1], s2.shape[-1])):
            for i in range(len(s1.shape[-1])):
                if s2.shape[-1][i] != "--":
                    s1.shape[-1][i] = s2.shape[-1][i]
            del s2
            return
        else:
            if len(s1.shape) + len(s2.shape) > 6:
                raise ValueError("The total number of sections must be 6 or less.")
            for i in range(len(s2.shape)):
                for j in range(len(s2.shape[i])):
                    if s2.shape[i][j][0] == "c":
                        s2.shape[i][j] = "--"
            s1.shape = s1.shape + s2.shape
            del s2
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
        if s1.layers <= s2.layers:
            for i in range(len(s1.shape)):
                new_shape_1 = s1.shape[i][0:3] + s2.shape[i][3:]
                new_shape_2 = s2.shape[i][0:3] + s1.shape[i][3:]
                s1.shape[i] = new_shape_1
                s2.shape[i] = new_shape_2
            for i in range(s2.layers - s1.layers):
                s1.shape.append(["--", "--", "--"] + s2.shape[i][3:])
            return
        else:
            for i in range(len(s2.shape)):
                new_shape_1 = s2.shape[i][0:3] + s1.shape[i][3:]
                new_shape_2 = s1.shape[i][0:3] + s2.shape[i][3:]
                s1.shape[i] = new_shape_1
                s2.shape[i] = new_shape_2
            for i in range(s1.layers - s2.layers):
                s2.shape.append(["--", "--", "--"] + s1.shape[s2.layers + i][3:])
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
        
class shape:
    def __init__(self, shape_code:str):
        self.shape = self.decode_shape(shape_code)
        self.layers = len(self.shape)

    def decode_shape(self, shape_code:str):
        s = []
        if ":" in shape_code:
            layers = shape_code.split(':')
        else:
            layers = [shape_code]
        for f in layers:
            layer = [f[i:i+2] for i in range(0, len(f), 2)]
            s.append(layer)
        return s

    def __str__(self):
        # Flatten the nested lists and concatenate the string pairs
        return ':'.join([''.join(layer) for layer in self.shape])

s1 = shape('HuP-ccFucmGm:GbGucrP-GyP-:HuP-P-P-cyHy:HbGgGrFucmGk:HuFyFc------')
s2 = shape("------cgGbP-")