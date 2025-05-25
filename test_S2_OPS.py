import pytest
from S2_OPS import shape, machines

def test_decode_shape_single_layer():
    s = shape("HuFwGrHuFwGr")
    assert s.shape == [["Hu", "Fw", "Gr", "Hu", "Fw", "Gr"]]

def test_decode_shape_multi_layer():
    s = shape("HuFwGrHuFwGr:HuFwGrHuFwGr")
    assert s.shape == [["Hu", "Fw", "Gr", "Hu", "Fw", "Gr"], ["Hu", "Fw", "Gr", "Hu", "Fw", "Gr"]]

def test_str_method():
    s = shape("HuFwGrHuFwGr")
    assert str(s) == "HuFwGrHuFwGr"

def test_paint():
    s = shape("HuFwGrHuFwGr")
    machines.paint(s, "g")
    assert all(x.endswith("g") or x == "--" or x == "P-" for x in s.shape[-1])

def test_gen_crystal():
    s = shape("------------")
    machines.gen_crystal(s, "b")
    assert all(x == "cb" for x in s.shape[0])

def test_stack_simple():
    s1 = shape("HuFwGrHuFwGr")
    s2 = shape("HwHwFrFrGuGu")
    machines.stack(s1, s2)
    assert len(s1.shape) == 2
    assert s1.shape == [
        ["Hu", "Fw", "Gr", "Hu", "Fw", "Gr"],
        ["Hw", "Hw", "Fr", "Fr", "Gu", "Gu"]
    ]

def test_stack_complex_1():
    s1 = shape("P-P-P-P-P-P-:Hu--HuP-----:------Hu----:crHucrHu----")
    s2 = shape("P-P-HuP-P-P-:Hu----P-----:------P-----:crHucrHu----")
    machines.stack(s1, s2)
    assert s1.shape == [
        [ "P-", "P-", "P-", "P-", "P-", "P-" ],
        [ "Hu", "--", "Hu", "P-", "P-", "P-" ],
        [ "--", "--", "--", "Hu", "--", "--" ],
        [ "cr", "Hu", "cr", "Hu", "--", "--" ],
        [ "P-", "P-", "Hu", "P-", "--", "--" ],
        [ "Hu", "Hu", "--", "P-", "--", "--" ]
    ]

def test_stack_complex_2():
    s1 = shape("P-----------")
    s2 = shape("HuHu--------:--HuHu------:----HuHu----:------HuHu--:--------HuHu")
    machines.stack(s1, s2)
    assert s1.shape == [
        ['P-', '--', '--', '--', '--', '--'], 
        ['Hu', 'Hu', '--', '--', '--', '--'], 
        ['--', 'Hu', 'Hu', '--', '--', '--'], 
        ['--', '--', 'Hu', 'Hu', '--', '--'], 
        ['--', '--', '--', 'Hu', 'Hu', '--'], 
        ['--', '--', '--', '--', 'Hu', 'Hu']
    ]

def test_stack_with_crystal_removal():
    s1 = shape("HuFwGrHuFwGr")
    s2 = shape("HuHuHucrcrcr")
    machines.stack(s1, s2)
    assert s1.shape == [
        ["Hu", "Fw", "Gr", "Hu", "Fw", "Gr"],
        ["Hu", "Hu", "Hu", "--", "--", "--"]
    ]

def test_swap_equal_layers():
    s1 = shape("HrHrHrHrHrHr")
    s2 = shape("GwGwGwGwGwGw")
    machines.swap(s1, s2)
    assert s1.shape[0] == [
        "Hr","Hr", "Hr", "Gw", "Gw", "Gw"
    ]
    assert s2.shape[0] == [
        "Gw", "Gw", "Gw", "Hr","Hr", "Hr"
    ]

def test_rotate_cw():
    s = shape("HwHwFrFrGuGu")
    machines.rotate_cw(s)
    assert s.shape[0] == [ "Gu", "Hw", "Hw", "Fr", "Fr", "Gu"]

def test_rotate_ccw():
    s = shape("HwHwFrFrGuGu")
    machines.rotate_ccw(s)
    assert s.shape[0] == [ "Hw", "Fr", "Fr", "Gu", "Gu", "Hw", ]

def test_rotate_180():
    s = shape("HwHwFrFrGuGu")
    machines.rotate_180(s)
    assert s.shape[0] == ["Fr", "Gu", "Gu", "Hw", "Hw", "Fr"]

def test_pin_adds_pin_layer():
    s1 = shape("HwHwFrFrGuGu")
    s2 = shape("HwHwFr--GuGu")
    machines.pin(s1)
    machines.pin(s2)
    assert len(s1.shape) == 2
    assert len(s2.shape) == 2
    assert s1.shape[0].count("P-") == 6
    assert s2.shape[0].count("P-") == 5