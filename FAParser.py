import collections
from typing import Dict, Tuple, Set, List
import os


class FiniteAutomaton:
    def __init__(self, initialState: str, states: Set[str], finalStates: Set[str], alphabet: Set[str], transitions: Dict[Tuple[str, str], List[str]]):
        self.initialState = initialState
        self.states = states
        self.finalStates = finalStates
        self.alphabet = alphabet
        self.transitions = transitions

    def checkIfDeterministic(self) -> bool:
        for (state1, character), state2 in self.transitions.items():
            if len(state2) > 1:
                return False
        return True



def FAParser(filename: str) -> FiniteAutomaton:
    FA = FiniteAutomaton("", set(), set(), set(), collections.defaultdict(list))
    with open(filename, "r") as f:
        states = f.readline().split()
        FA.initialState = states[0]
        FA.states = set(states)
        FA.finalStates = set(f.readline().split())
        FA.alphabet = set(f.readline().split())
        while f:
            transition = f.readline().split()
            if not transition:
                break
            state1 = transition[0]
            character = transition[1]
            state2 = transition[2]
            FA.transitions[(state1, character)].append(state2)

    return FA

def stringAsDelta(entry: Tuple[Tuple[str, str], List[str]]) -> str:
    state = "Epsilon" if len(entry[1]) == 0 else entry[1][0]
    return 'delta({0}, {1}) -> {2}'.format(entry[0][0], entry[0][1], state)

def getTransitions(FA: FiniteAutomaton) -> str:
    res = ""
    for entry in FA.transitions.items():
        res += stringAsDelta(entry) + "\n"
    return res

if __name__ == '__main__':
    FA = FAParser('number_constant_FA.in')

    menu = """1. Show states
2. Show final states
3. Show alphabet
4. Show transitions
5. Check if sequence is accepted by the FA
0. Exit"""

    def trySequence():
        if not FA.checkIfDeterministic():
            print("Non deterministic!")
            return ""
        sequence = input("Sequence = ")
        idx = 0
        currentState = FA.initialState
        if len(sequence) == 0:
            if currentState in FA.finalStates:
                print(stringAsDelta(((currentState, "Epsilon"), ["Epsilon"])))
                return ""
            else:
                print("Not accepted!")
                return ""
        for char in sequence:
            if char not in FA.alphabet:
                print("Sequence contains elements that are not in the alphabet!")
                return ""
            states = FA.transitions[(currentState, char)]
            if len(states) == 0:
                print("Not accepted!")
                return ""
            print(stringAsDelta(((currentState, sequence[idx:]), states)))
            idx += 1
            currentState = states[0]
        print(stringAsDelta(((currentState, "Epsilon"), ["Epsilon"])))
        return ""

    commands = {
        1: lambda: FA.states,
        2: lambda: FA.finalStates,
        3: lambda: FA.alphabet,
        4: lambda: getTransitions(FA),
        5: lambda: trySequence(),
        0: lambda: exit(0)
    }
    while True:
        command = input(menu + "\n")
        try:
            command = int(command, base=10)
        except ValueError:
            command = -1

        try:
            print(commands[command]())
        except KeyError:
            print("Wrong command!")
