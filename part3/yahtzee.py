"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
Raghav Atreya
raghavatreya16@gmail.com

http://www.codeskulptor.org/#user46_cPbL3pWvsfyIYuS_11.py

tip
https://www.coursera.org/learn/principles-of-computing-1/discussions/weeks/4/threads/JH6-HwfAEeaGYRLQcnuUpQ
https://www.coursera.org/learn/principles-of-computing-1/discussions/all/threads/JH6-HwfAEeaGYRLQcnuUpQ/replies/jWxZUAfXEeaFxAruJmtipQ/comments/V8VcGg6FEeaO1w7d1s7iLw
https://www.coursera.org/learn/principles-of-computing-1/discussions/weeks/4/threads/pxRGLMd6EeaQDgq_dR_6Tg
https://www.coursera.org/learn/principles-of-computing-1/discussions/weeks/4/threads/pxRGLMd6EeaQDgq_dR_6Tg/replies/k0UmV8fWEeasiQ5A6jAKtA
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(50)




def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand, a tuple of dice value

    Returns an integer score 
    """
    
    value = {}
    for ind in range(1, max(hand)+1):
        value[ind] = 0
    
    for ele in hand:
        value[ele] += ele
    val = -1
    for ele in value:
        if value[ele] > val:
            val = value[ele]

    return val


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    Compute the score of each hand you can form with these two fixed dice and the three other ones 
    and divide by the number of hands to get the expected value of the random variable score.
    """
    total = 0
    counter = 0
    for ele in gen_all_sequences(range(1, num_die_sides+1), num_free_dice):
        counter += 1
        total += score(ele+held_dice)
    
    return float(total) / counter


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """

    from_hand = [()]
    for item in hand:
        for subset in from_hand:
            from_hand = from_hand + [tuple(subset) + (item, )]
           
    return set(from_hand)
            




def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    answer = (-1.0, ())
    
    for item in gen_all_holds(hand):
        value = expected_value(item, num_die_sides, len(hand)-len(item))
        if answer[0] < value:
            answer = (value, item)
            
    return answer


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    

# comment run_example before submitting the grader
# run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
