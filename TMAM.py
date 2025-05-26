import S2_OPS as S_
# SHAPEZ 2 what we know
# only allows for "extended" boolean math
# AND, OR, NOT, XOR, EQ

# Digital shape handling
# Rotator, Half Destroyer, Stacker, Unstacker, Painter, Crystal Generator, Swapper, Pin pusher, and shape analyzer

# shape analyzer takes one input and returns LEFT: COLOR, TOP: SHAPE

# TMAM is a true MAM shaped after a CMAM (Corner MAM) with more tricks to accomplish short commings of a CMAM.

#INPUT > str  | a VALID shapez 2 shape code only in hex format up to 6 layers
INPUT = "P-----------:HuHu--------:--HuHu------:----HuHu----:------HuHu--:--------HuHu"
# Desired output is a way to decode shapes and edge cases in order to create a sequence of operations to achecive input shape.
# Swapping corners covers a lot of edge cases due to it allowing floating shapes but does not allow for floating pins and crytals built in this manner tend to over flow.
# Hanging crystals can exist through the use of claw and hyrbid methods described in the S2 Discord

class TMAM:
    def __init__(self, input_shape_code: str):
        self.input_shape = S_(input_shape_code)
        

