"""
This class is intended to take care of the reinforcement learning.
It uses a naive approach where it tries to match a category based
on a simple policy that we constructed.
"""

def iterative_learning(alpha, beta, correct_category, text_to_analyze):
    """
    iterative_learning is the method that brute forces its way to a local
    (and potentially global) maximum for correctly determining the category
    """
    #Call get_word_statistics(text_to_analyze)
    return alpha * beta * correct_category * text_to_analyze

def best_matching_category(categories, text_to_test):
    """
    return the max score matching from the categories and category_to_test
    """
    category_scores = []
    for category in categories:
        current_category_score = 0
        #compare top word occurences with the category_to_test
        for word in category:
            #if word occurence is within 3% of the category_to_test,add to score
            print("TODO" + word + text_to_test)
        category_scores.append(current_category_score)

    return category_scores.index(max(category_scores))
