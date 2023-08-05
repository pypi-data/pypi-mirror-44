import operator as op
import pytest

from itertools import permutations

from sweetpea import fully_cross_block
from sweetpea.primitives import Factor, DerivedLevel, WithinTrial, Transition, Window
from sweetpea.blocks import FullyCrossBlock
from sweetpea.constraints import Exclude

color = Factor("color", ["red", "blue"])
text  = Factor("text",  ["red", "blue"])
size  = Factor("size",  ["big", "small", "tiny"])
direction = Factor("direction", ["up", "down"])

con_level  = DerivedLevel("con", WithinTrial(op.eq, [color, text]))
inc_level  = DerivedLevel("inc", WithinTrial(op.ne, [color, text]))
con_factor = Factor("congruent?", [con_level, inc_level])

color_repeats_factor = Factor("repeated color?", [
    DerivedLevel("yes", Transition(lambda colors: colors[0] == colors[1], [color])),
    DerivedLevel("no",  Transition(lambda colors: colors[0] != colors[1], [color]))
])

text_repeats_factor = Factor("repeated text?", [
    DerivedLevel("yes", Transition(lambda texts: texts[0] == texts[1], [text])),
    DerivedLevel("no",  Transition(lambda texts: texts[0] != texts[1], [text]))
])

congruent_bookend = Factor("congruent bookend?", [
    DerivedLevel("yes", Window(lambda color, text: color == text, [color, text], 1, 3)),
    DerivedLevel("no",  Window(lambda color, text: color != text, [color, text], 1, 3))
])

color3 = Factor("color3", ["red", "blue", "green"])

yes_fn = lambda colors: colors[0] == colors[1] == colors[2]
no_fn = lambda colors: not yes_fn(colors)
color3_repeats_factor = Factor("color3 repeats?", [
    DerivedLevel("yes", Window(yes_fn, [color3], 3, 1)),
    DerivedLevel("no",  Window(no_fn, [color3], 3, 1))
])


def test_get_factor():
    block = fully_cross_block([color, text], [color, text], [])

    assert block.get_factor("color") == color
    assert block.get_factor("bogus") == None


@pytest.mark.parametrize('design,expected',
    [([color, text, color_repeats_factor, text_repeats_factor], [0, 2, 16, 22]),
     ([color, text, text_repeats_factor, color_repeats_factor], [0, 2, 22, 16]),
     ([color_repeats_factor, text, color, text_repeats_factor], [2, 0, 16, 22]),
     ([text_repeats_factor, text, color, color_repeats_factor], [2, 0, 22, 16])])
def test_fully_cross_block_first_variable_for_factor(design, expected):
    block = fully_cross_block(design, [color, text], [])

    assert block.first_variable_for_level("color", "red") == expected[0]
    assert block.first_variable_for_level("color", "blue") == expected[0] + 1
    assert block.first_variable_for_level("text", "red") == expected[1]
    assert block.first_variable_for_level("text", "blue") == expected[1] + 1
    assert block.first_variable_for_level("repeated color?", "yes") == expected[2]
    assert block.first_variable_for_level("repeated color?", "no") == expected[2] + 1
    assert block.first_variable_for_level("repeated text?", "yes") == expected[3]
    assert block.first_variable_for_level("repeated text?", "no") == expected[3] + 1


def test_fully_cross_block_first_variable_for_factor_with_color3():
    block = fully_cross_block([color3_repeats_factor, color3, text], [color3, text], [])

    assert block.first_variable_for_level("color3 repeats?", "yes") == 30
    assert block.first_variable_for_level("color3 repeats?", "no") == 31


def test_factor_variables_for_trial():
    block = fully_cross_block([color, text, color_repeats_factor], [color, text], [])

    assert block.factor_variables_for_trial(color, 1) == [1, 2]
    assert block.factor_variables_for_trial(color, 4) == [13, 14]

    assert block.factor_variables_for_trial(text, 2) == [7, 8]

    assert block.factor_variables_for_trial(color_repeats_factor, 2) == [17, 18]
    assert block.factor_variables_for_trial(color_repeats_factor, 4) == [21, 22]


def test_factor_variables_for_trial_with_expanded_crossing():
    # Because a transition is included in the crossing, this design requires 5 trials.
    block = fully_cross_block([color, text, color_repeats_factor], [text, color_repeats_factor], [])

    assert block.factor_variables_for_trial(color, 1) == [1, 2]
    assert block.factor_variables_for_trial(color, 5) == [17, 18]

    assert block.factor_variables_for_trial(text, 2) == [7, 8]
    assert block.factor_variables_for_trial(text, 5) == [19, 20]

    assert block.factor_variables_for_trial(color_repeats_factor, 2) == [21, 22]
    assert block.factor_variables_for_trial(color_repeats_factor, 4) == [25, 26]
    assert block.factor_variables_for_trial(color_repeats_factor, 5) == [27, 28]


def test_variable_list_for_trial():

    # ---------------------------------------------------
    # |   Trial |  color   |   text   | repeated color? |
    # |       # | red blue | red blue |   yes      no   |
    # ---------------------------------------------------
    # |       1 |  1   2   |  3   4   |                 |
    # |       2 |  5   6   |  7   8   |    17      18   |
    # |       3 |  9   10  | 11   12  |    19      20   |
    # |       4 | 13   14  | 15   16  |    21      22   |
    # ---------------------------------------------------
    block = fully_cross_block([color, text, color_repeats_factor], [color, text], [])

    assert block.variable_list_for_trial(1) == [[ 1, 2 ], [ 3, 4 ], []]
    assert block.variable_list_for_trial(2) == [[ 5, 6 ], [ 7, 8 ], [17, 18]]
    assert block.variable_list_for_trial(3) == [[ 9, 10], [11, 12], [19, 20]]
    assert block.variable_list_for_trial(4) == [[13, 14], [15, 16], [21, 22]]


def test_block_get_variable():
    block = fully_cross_block([color, text, color_repeats_factor], [color, text], [])

    assert block.get_variable(1, ("color", "red")) == 1
    assert block.get_variable(1, ("color", "blue")) == 2
    assert block.get_variable(3, ("color", "red")) == 9
    assert block.get_variable(3, ("color", "blue")) == 10

    assert block.get_variable(2, ("text", "red")) == 7
    assert block.get_variable(2, ("text", "blue")) == 8
    assert block.get_variable(3, ("text", "red")) == 11
    assert block.get_variable(3, ("text", "blue")) == 12


def test_fully_cross_block_decode_variable():
    block = fully_cross_block([color, text, color_repeats_factor, text_repeats_factor],
                              [color, text],
                              [])

    assert block.decode_variable(1) == ("color", "red")
    assert block.decode_variable(2) == ("color", "blue")
    assert block.decode_variable(5) == ("color", "red")
    assert block.decode_variable(14) == ("color", "blue")

    assert block.decode_variable(3) == ("text", "red")
    assert block.decode_variable(4) == ("text", "blue")
    assert block.decode_variable(15) == ("text", "red")
    assert block.decode_variable(12) == ("text", "blue")

    assert block.decode_variable(17) == ("repeated color?", "yes")
    assert block.decode_variable(18) == ("repeated color?", "no")
    assert block.decode_variable(19) == ("repeated color?", "yes")
    assert block.decode_variable(22) == ("repeated color?", "no")

    assert block.decode_variable(23) == ("repeated text?", "yes")
    assert block.decode_variable(24) == ("repeated text?", "no")
    assert block.decode_variable(27) == ("repeated text?", "yes")
    assert block.decode_variable(28) == ("repeated text?", "no")


def test_fully_cross_block_decode_variable_with_transition_first():
    block = fully_cross_block([text_repeats_factor, text, color, color_repeats_factor],
                              [color, text],
                              [])

    assert block.decode_variable(1) == ("text", "red")
    assert block.decode_variable(2) == ("text", "blue")
    assert block.decode_variable(5) == ("text", "red")
    assert block.decode_variable(14) == ("text", "blue")

    assert block.decode_variable(3) == ("color", "red")
    assert block.decode_variable(4) == ("color", "blue")
    assert block.decode_variable(15) == ("color", "red")
    assert block.decode_variable(12) == ("color", "blue")

    assert block.decode_variable(17) == ("repeated text?", "yes")
    assert block.decode_variable(18) == ("repeated text?", "no")
    assert block.decode_variable(19) == ("repeated text?", "yes")
    assert block.decode_variable(22) == ("repeated text?", "no")

    assert block.decode_variable(23) == ("repeated color?", "yes")
    assert block.decode_variable(24) == ("repeated color?", "no")
    assert block.decode_variable(27) == ("repeated color?", "yes")
    assert block.decode_variable(28) == ("repeated color?", "no")


def test_fully_cross_block_decode_variable_with_general_window():
    block = fully_cross_block([color, text, congruent_bookend],
                              [color, text],
                              [])

    assert block.decode_variable(1) == ("color", "red")
    assert block.decode_variable(2) == ("color", "blue")
    assert block.decode_variable(5) == ("color", "red")
    assert block.decode_variable(14) == ("color", "blue")

    assert block.decode_variable(3) == ("text", "red")
    assert block.decode_variable(4) == ("text", "blue")
    assert block.decode_variable(15) == ("text", "red")
    assert block.decode_variable(12) == ("text", "blue")

    assert block.decode_variable(17) == ("congruent bookend?", "yes")
    assert block.decode_variable(18) == ("congruent bookend?", "no")
    assert block.decode_variable(19) == ("congruent bookend?", "yes")
    assert block.decode_variable(20) == ("congruent bookend?", "no")


def test_fully_cross_block_trials_per_sample():
    text_single  = Factor("text",  ["red"])

    assert FullyCrossBlock([color, text],
                           [color, text],
                           []).trials_per_sample() == 4
    assert FullyCrossBlock([color, text, direction],
                           [color, text, direction],
                           []).trials_per_sample() == 8
    assert FullyCrossBlock([size, text_single],
                           [size, text_single],
                           []).trials_per_sample() == 3
    assert FullyCrossBlock([size, color],
                           [size, color],
                           []).trials_per_sample() == 6
    assert FullyCrossBlock([text_single],
                           [text_single],
                           []).trials_per_sample() == 1

    assert FullyCrossBlock([color, text, color_repeats_factor], [color, text], []).trials_per_sample() == 4


def test_fully_cross_block_trials_per_sample_with_transition_in_crossing():
    block = fully_cross_block([color, text, color_repeats_factor],
                              [text, color_repeats_factor],
                              [])

    # Typically, only 4 trials are needed to cross two factors each with two levels. (2 * 2 = 4)
    # However, because one of these factors is a transition, it doesn't apply to the first trial.
    # As a result, we actually need 5 trials to do a full crossing between the two.
    assert block.trials_per_sample() == 5

    # The crossing size is still just 4.
    assert block.crossing_size() == 4

def test_fully_cross_block_variables_per_trial():
    assert FullyCrossBlock([color, text], [], []).variables_per_trial() == 4
    assert FullyCrossBlock([color, text, con_factor], [], []).variables_per_trial() == 6

    # Should exclude Transition and Windows from variables per trial count, as they don't always
    # have a representation in the first few trials. (Depending on the window width)
    assert FullyCrossBlock([color, text, color_repeats_factor],
                           [color, text],
                           []).variables_per_trial() == 4


def test_fully_cross_block_grid_variables():
    assert FullyCrossBlock([color, text, con_factor],
                           [color, text], []).grid_variables() == 24

    # Should include grid variables, as well as additional variables for complex windows.
    assert FullyCrossBlock([color, text, color_repeats_factor],
                           [color, text],
                           []).grid_variables() == 16


def test_fully_cross_block_variables_per_sample():
    assert FullyCrossBlock([color, text, con_factor],
                           [color, text], []).variables_per_sample() == 24

    # Should include grid variables, as well as additional variables for complex windows.
    assert FullyCrossBlock([color, text, color_repeats_factor],
                           [color, text],
                           []).variables_per_sample() == 22

    assert FullyCrossBlock([color, text, color_repeats_factor, text_repeats_factor],
                           [color, text],
                           []).variables_per_sample() == 28


def test_fully_cross_block_variables_for_factor():
    assert FullyCrossBlock([color, text], [color, text], []).variables_for_factor(color) == 8
    assert FullyCrossBlock([color, text], [color, text], []).variables_for_factor(text) == 8

    assert FullyCrossBlock([color, text, color_repeats_factor],
                           [color, text],
                           []).variables_for_factor(color_repeats_factor) == 6
    assert FullyCrossBlock([color, text, color_repeats_factor],
                           [color, text],
                           []).variables_for_factor(color_repeats_factor) == 6

    assert FullyCrossBlock([color3_repeats_factor, color3, text],
                           [color3, text],
                           []).variables_for_factor(color3) == 18

    assert FullyCrossBlock([color3_repeats_factor, color3, text],
                           [color3, text],
                           []).variables_for_factor(text) == 12

    assert FullyCrossBlock([color3_repeats_factor, color3, text],
                           [color3, text],
                           []).variables_for_factor(color3_repeats_factor) == 8

    assert FullyCrossBlock([color, text, congruent_bookend],
                           [color, text],
                           []).variables_for_factor(congruent_bookend) == 4


def test_fully_cross_block_crossing_size_with_exclude():
    # No congruent excludes 2 trials, 4 - 2 = 2
    assert FullyCrossBlock([color, text, con_factor],
                           [color, text],
                           [Exclude("congruent?", "con")],
                           require_complete_crossing=False).crossing_size() == 2


def test_fully_cross_block_crossing_size_with_overlapping_exclude():
    # How about with two overlapping exclude constraints? Initial crossing size
    # should be 3 x 3 = 9.
    # Excluding congruent pairs will reduce that to 9 - 3 = 6
    # Then excluding red and green on top of that should make it 5.
    color = Factor("color", ["red", "blue", "green"])
    text  = Factor("text",  ["red", "blue", "green"])

    congruent_factor = Factor("congruent?", [
        DerivedLevel("congruent", WithinTrial(op.eq, [color, text])),
        DerivedLevel("incongruent", WithinTrial(op.ne, [color, text])),
    ])

    def illegal(color, text):
        return (color == "red" and text == "green") or color == text

    def legal(color, text):
        return not illegal(color, text)

    legal_factor = Factor("legal", [
        DerivedLevel("yes", WithinTrial(legal, [color, text])),
        DerivedLevel("no",  WithinTrial(illegal, [color, text]))
    ])

    assert FullyCrossBlock([color, text, congruent_factor, legal_factor],
                           [color, text],
                           [Exclude("congruent?", "congruent"), # Excludes 3
                            Exclude("legal", "no")], # Exludes 4, but 3 were already excluded
                           require_complete_crossing=False).crossing_size() == 5


def test_fully_cross_block_should_copy_input_lists():
    # FullyCrossBlock should copy the input lists, so as not to break if the
    # user modifies the original list.
    design = [color, text, con_factor]
    crossing = [color, text]
    constraints = [Exclude("congruent?", "con")]

    block = FullyCrossBlock(design, crossing, constraints)

    design.clear()
    assert len(block.design) == 3

    crossing.clear()
    assert len(block.crossing) == 2

    constraints.clear()
    assert len(block.constraints) == 1


def test_build_variable_list_for_simple_factors():
    block = fully_cross_block([color, text, con_factor], [color, text], [])

    assert block.build_variable_list(("color", "red")) == [1, 7, 13, 19]
    assert block.build_variable_list(("congruent?", "con")) == [5, 11, 17, 23]


def test_build_variable_list_for_complex_factors():
    block = fully_cross_block([color, text, color_repeats_factor], [color, text], [])

    assert block.build_variable_list(("repeated color?", "yes")) == [17, 19, 21]
    assert block.build_variable_list(("repeated color?", "no"))  == [18, 20, 22]


def test_build_variable_list_for_three_derived_levels():
    def count_diff(colors, texts):
        changes = 0
        if (colors[0] != colors[1]): changes += 1
        if (texts[0] != texts[1]): changes += 1
        return changes

    def make_k_diff_level(k):
        def k_diff(colors, texts):
            return count_diff(colors, texts) == k
        return DerivedLevel(str(k), Transition(k_diff, [color, text]))

    changed = Factor("changed", [make_k_diff_level(0),
                                 make_k_diff_level(1),
                                 make_k_diff_level(2)]);

    block = fully_cross_block([color, text, changed], [color, text], [])

    assert block.build_variable_list(("changed", "0")) == [17, 20, 23]
    assert block.build_variable_list(("changed", "1")) == [18, 21, 24]
    assert block.build_variable_list(("changed", "2")) == [19, 22, 25]
