# (c) 2012-2018 Dativa, all rights reserved
# -----------------------------------------
#  This code is licensed under MIT license (see license.txt for details)

#!python
#cython: language_level=3, boundscheck=False, wraparound=False, optimize.use_switch=True
cimport numpy as np
import numpy as np
import Levenshtein

"""
Contains optimized string distance functions for the best matches and lookalike matches
Contains .pxd file to compile with cython
"""

# def get_distance(word_1, word_2):
cdef inline double get_distance(str word_1, str word_2):
    cdef double d
    cdef int length_1
    """
    Returns an estimate of the similarity of strings,
    where 1.0 means they are identical an 0 means they
    are totally disimillar.

    For single words, uses the jaro_winkler distance,
    Otherwise use metric based on the Leveshtein distance
    """

    length_1 = len(word_1)

    if length_1 > 15:
        d = Levenshtein.distance(word_1, word_2) / length_1
        if d > 1:
            return 0
        else:
            return 1 - d
    else:
        return Levenshtein.jaro_winkler(word_1, word_2)

# def which_pass(cycle, string_1, string_2, string_1_length, string_2_length):
cdef inline int which_pass(int cycle, str string_1, str string_2, int string_1_length, int string_2_length):
    """
    Both the best matches and the lookalike match implement a multi-pass process
    as follows:
    1. Match only strings of comparable length of more than 1 character in length or
       where the first and second letters match
    2. Match strings of comparable length where the first letter matches
    3. Match strings where the first letter matches
    4. Match strings where the length is comparable
    5. Match all others that are not more that twice the length of each other

    Parameters:
    cycle: the cycle to check eligbility against
    string_1: the first string
    string_2: the second string
    string_1_length: the optional length of the first string
    string_2_length: the optional length fo the second string
    """

    if cycle == 1:
        if string_2_length == 1 and string_1_length == 1:
            return True
        else:
            return abs(string_2_length - string_1_length) < 3 and string_2[0] == string_1[0] and string_2[1] == \
                   string_1[1]
    elif cycle == 2:
        return abs(string_2_length - string_1_length) < 3 and string_2[0] == string_1[0]

    elif cycle == 3:
        return string_2[0] == string_1[0]

    elif cycle == 4:
        return abs(string_2_length - string_1_length) < 3

    elif cycle == 5:
        return string_1_length < string_2_length * 2 and string_2_length < string_1_length * 2
    else:
        return False

# def which_pass_no_length(cycle, string_1, string_2):
cdef inline int which_pass_no_length(int cycle, str string_1, str string_2):
    """
    Provides a wrapper or which_pass when no string length is cached
    """
    return which_pass(cycle, string_1, string_2, len(string_1), len(string_2))

# def get_closest_match(string_list, possible_values, threshold=0.7):
cpdef np.ndarray get_closest_match(np.ndarray[object, ndim=1] string_list, np.ndarray[object, ndim=1] possible_values,
                                   double threshold=0.7):
    cdef np.ndarray[object, ndim=1] results  # noqa
    cdef np.ndarray[np.float_t, ndim=1] distances  # noqa
    cdef np.ndarray[np.float_t, ndim=1] ref_distances  # noqa
    cdef np.ndarray[np.int_t, ndim=1] ref_lengths  # noqa
    cdef Py_ssize_t string_ix
    cdef Py_ssize_t possible_ix
    cdef Py_ssize_t string_length
    cdef Py_ssize_t target_ix
    cdef int cycle

    """
    Takes a list containing strings to be matched against a set of possible
    values and returns a matrstring_ix matching the two to the closest values,
    provided the string similarity is less than the specified threshold

    Parameters
    ----------

    string_list : the list containing the strings to be compared
    possible_values : an array of possible values the string can take
    threshold: the string similarity threshold

    """

    results = np.zeros(len(string_list), dtype=object)
    distances = np.zeros((len(string_list)), dtype=np.float)
    ref_distances = np.zeros((len(possible_values)), dtype=np.float)
    ref_lengths = np.zeros((len(possible_values)), dtype=np.int)

    for string_ix in range(0, len(possible_values)):
        ref_lengths[string_ix] = len(possible_values[string_ix])

    for string_ix in range(0, len(string_list)):
        string_length = len(string_list[string_ix])

        # cycle through the reference list in four passes
        for cycle in [1, 2, 3, 4, 5]:
            # continue only while we don't have match that is above the
            # threshold
            if distances[string_ix] < threshold:
                # cycle through every row and calculate the distance
                ref_distances.fill(0)
                for possible_ix in range(0, len(possible_values)):
                    if which_pass(cycle,
                                  possible_values[possible_ix],
                                  string_list[string_ix],
                                  ref_lengths[possible_ix],
                                  string_length):
                        ref_distances[possible_ix] = get_distance(possible_values[possible_ix], string_list[string_ix])

                # get the closest match
                target_ix = np.argsort(ref_distances)[len(possible_values) - 1]
                results[string_ix] = possible_values[target_ix]
                distances[string_ix] = ref_distances[target_ix]

    return np.vstack((results, distances))

# def run_lookalike(matrix, rows_to_match=None, top_n=5, threshold=0.7):
cpdef np.ndarray run_lookalike(np.ndarray matrix,
                               np.ndarray rows_to_match,
                               int top_n=5,
                               double threshold=0.7):
    cdef np.ndarray reference
    cdef np.ndarray choices
    cdef np.ndarray uniques
    cdef np.ndarray unique_counts
    cdef np.ndarray sort
    cdef Py_ssize_t result_column
    cdef Py_ssize_t distance_column
    cdef Py_ssize_t match_column
    cdef Py_ssize_t first_column
    cdef Py_ssize_t last_column
    cdef Py_ssize_t number_rows
    cdef int cycle
    cdef int row_pass
    cdef Py_ssize_t number_uniques
    """
    Runs a lookalike match on the passed matrix and returns as an array from
    the final column in the matrix. The lookalike column works by scanning
    through all comparable columns looking for the top n most similar columns.
    It then counts the frequency of each result and chooses the most popular.

    Parameters
    ----------
    matrix:  A numpy matrix containing:
        - the strings to be used for the lookalike match
        - the values of the target field
        - a blank column of int64, which will contain the distances
        - a blank column of strings, the will contain the result
    rows_to_match: an array specifying which rows need to be matched
    top_n: the number of matches to be compared
    threshold: the string similarity threshold for comparisons
    """
    # useful variable for tracking the columns in the matrix
    result_column = matrix.shape[0] - 1
    distance_column = matrix.shape[0] - 2
    match_column = matrix.shape[0] - 3
    first_column = 0

    # the last column contains the distance calculation
    last_column = matrix.shape[0] - 3
    number_rows = matrix.shape[1]

    # iterate through every row in the matrix
    for ix in range(0, number_rows):

        # if do not need to match this
        if rows_to_match is None or rows_to_match[ix]:
            # grab the reference row
            reference = np.transpose(matrix)[ix]

            # cycle through every row and calculate the distance
            for cycle in [1, 2, 3, 5]:
                if matrix[distance_column, matrix[distance_column] > threshold * (last_column - first_column)].shape[
                    0] - 1 < top_n:
                    for row_ix in range(0, number_rows):
                        if (rows_to_match is not None and rows_to_match[row_ix]) or row_ix == ix:
                            matrix[distance_column, row_ix] = 100
                        else:
                            row_pass = 0
                            for col_ix in range(first_column, last_column):
                                row_pass = row_pass + \
                                           which_pass_no_length(cycle,
                                                                reference[col_ix],
                                                                matrix[col_ix][row_ix])

                            if cycle == round(row_pass / (last_column - first_column)):
                                total_distance = 0
                                for col_ix in range(first_column, last_column):
                                    d = get_distance(
                                        reference[col_ix], matrix[col_ix][row_ix])
                                    total_distance = total_distance + \
                                                     (1 - d) * (1 - d)

                                matrix[distance_column,
                                       row_ix] = total_distance

            # choose amongst the most popular of the top_n neighbours
            choices = matrix[match_column][np.argsort(matrix[distance_column])[:top_n]]
            uniques, unique_counts = np.unique(choices, return_counts=True)
            number_uniques = len(uniques)
            if number_uniques > 1:
                sort = unique_counts.argsort()
                if unique_counts[sort[number_uniques - 1]] > unique_counts[sort[number_uniques - 2]]:
                    matrix[result_column, ix] = uniques[sort][number_uniques - 1]
                else:
                    for i in range(0, len(choices)):
                        if choices[i] == uniques[sort[number_uniques - 1]] or choices[i] == uniques[
                            sort[number_uniques - 2]]:
                            matrix[result_column, ix] = choices[i]
                            break
            elif number_uniques == 1:
                matrix[result_column, ix] = uniques[0]

    return matrix[result_column]
