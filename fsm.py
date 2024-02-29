import string

from dataclasses import dataclass, field

@dataclass
class FSM:
    """
    This FSM class uses transition tables to run finite-state machines to check
    whether a string matches a regular expression pattern.
    Each finite-state machine requires the following:
    1. transition table: a matrix with transitions
    2. alphabet: a dictionary that maps all possible symbols to their column
       in the transition table
    3. accepted states: a set with all accepted states
    """

    def run_fsm(self, transition_table, alphabet, accepted_states, w):
        """
        Run the finite-state machine on the string w using the passed in
        transition table, alphabet, and accepted states.
        Return True if finite-state machine ends in an accepted state, False
        otherwise. Return False if w contains a symbol not found in alphabet.
        Note: No need to modify this method when adding new patterns.
        """
        state = 0
        for i in range(len(w)):
            curr_symbol = w[i]
            # Return False if current symbol not in alphabet
            if curr_symbol not in alphabet:
                return False
            # Transition to next state
            col = alphabet[curr_symbol]
            state = transition_table[state][col]
        if state in accepted_states:
            return True
        else:
            return False

    def is_real(self, w):
        """Return True if the string w is a real number, False otherwise"""
        # Transition table for real number. RE: d+.d+
        real_tt = [
            [1, 4],
            [1, 2],
            [3, 4],
            [3, 4],
            [4, 4]
        ]

        # Alphabet map for real numbers. Maps symbols to column in
        # transition table
        # digits are all col 0; '.' is col 1
        real_alpha = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0,
                      '7': 0, '8': 0, '9': 0, '.': 1}

        # Accepted states for real numbers
        real_accepted = set([3])

        # Run FSM on string w and return result
        is_accepted = self.run_fsm(real_tt, real_alpha, real_accepted, w)
        return is_accepted

    def is_identifier(self, w):
        """Return True if the string w is an identifier, False otherwise"""
        # Transition table for identifier. RE: l(l|d|_)*
        identifier_tt = [
            [1, 5, 5],
            [2, 3, 4],
            [2, 3, 4],
            [2, 3, 4],
            [2, 3, 4],
            [5, 5, 5],
        ]

        # Alphabet map for identifiers. Maps symbols to column in
        # transition table
        # letters are col 0, digits are col 1, underscore is col 2
        identifier_alpha = {char: 0 for char in string.ascii_uppercase}
        identifier_alpha.update({char: 0 for char in string.ascii_lowercase})
        identifier_alpha.update({digit: 1 for digit in string.digits})
        identifier_alpha['_'] = 2

        # Accepted states for real numbers
        identifier_accepted = set([1,2,3,4])

        # Run FSM on string w and return result
        is_accepted = self.run_fsm(identifier_tt, identifier_alpha, identifier_accepted, w)
        return is_accepted
