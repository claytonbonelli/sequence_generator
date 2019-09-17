import exrex


class Sequence:
    """
    A sequence is a group of numbers and / or letters that will form a single character. This character will be changed
    using the given pattern, so if you need to create a string, for example with the following letters C3P6, the first
    time the "next" and "get" methods are executed, the result will be the letter C " The next run will return the
    digit "3", the next run the letter "P" and finally the next run will return the digit "6".
    The purpose of this class is therefore to return one character at a time, using the character set entered in
    the sequence, and each of the characters entered will be returned at each execution of the "next" and "get" methods.
    When all characters have been returned, a next execution of the "next" and "get" methods will restart the sequence.
    """
    OVERFLOW = 0
    UNDERFLOW = 1

    def __init__(self, sequence, parent=None):
        self.sequence = sequence
        self.index = -1
        self.parent = parent

    def send(self, *args, **kwargs):
        """
        Send a message for this class.
        """
        raise NotImplemented()

    def send_to_parent(self, *args, **kwargs):
        """
        Send a message for the parent.
        """
        if self.parent:
            self.parent.send(self, *args, **kwargs)

    def set(self, value):
        """
        Set the current sequence.
        :param value: the next sequence.
        """
        old = self.get()
        if old == value:
            return
        while True:
            v = self.next().get()
            if v == value:
                return
            if v == old:
                raise Exception("Impossible to set the value")

    def get(self):
        """
        :return: the current sequence's value.
        """
        if self.index == -1:
            self.index = 0
        return self.sequence[self.index]

    def previous(self):
        """
        Return to the previous sequence.
        :return: self
        """
        self.index -= 1
        size = len(self.sequence)
        if self.index >= 0:
            return self
        self.index = size - 1
        self.send_to_parent(flow=self.UNDERFLOW)
        return self

    def next(self):
        """
        Advance to the next sequence.
        :return: self
        """
        self.index += 1
        if self.index < len(self.sequence):
            return self
        self.index = 0
        self.send_to_parent(flow=self.OVERFLOW)
        return self


class Sequences(Sequence):
    """
    A list of sequences whose values will be returned incrementally according to the entered pattern. One such sequence
    pattern could be, for example, as follows:

    AA00
    AA01
    AA02
    AA99
    AE01
    AE02
    AE99
    AI01
    ...
    UU98
    UU99
    AA00

    To create a pattern consisting of 4 characters, with letters being sequences of vowels and
    numbers formed by digits 0-9, just do the following:

    s = Sequences (
        Sequence ("AEIOU"),
        Sequence ("AEIOU"),
        Sequence ("0123456789"),
        Sequence ("0123456789"),
    )
    """
    def __init__(self, sequence, parent=None):
        super().__init__(sequence, parent)
        self.indexes = []
        self.build_indexes()

    def build_indexes(self):
        if self.sequence is None or len(self.sequence) <= 0:
            return
        for index, value in enumerate(self.sequence):
            if not isinstance(value, Sequence):
                continue
            value.parent = self
            self.indexes.append(index)

    def send(self, *args, **kwargs):
        size = len(self.indexes)
        if size <= 0:
            return

        flow = kwargs.get('flow')
        sequence = args[0]

        if flow == self.OVERFLOW:
            for index, idx in enumerate(self.indexes):
                if self.sequence[idx] != sequence:
                    continue
                if index > 0:
                    self.sequence[self.indexes[index - 1]].next()
                    return
                # index == 0
                self.send_to_parent(flow=flow)

        elif flow == self.UNDERFLOW:
            for index, idx in enumerate(self.indexes):
                if self.sequence[idx] != sequence:
                    continue
                if index > 0:
                    self.sequence[self.indexes[index - 1]].previous()
                    return
                # index == 0
                self.send_to_parent(flow=flow)
            return

    def get(self):
        result = ''
        for value in self.sequence:
            if isinstance(value, Sequence):
                result += str(value.get())
            else:
                result += value
        return result

    def previous(self):
        if len(self.indexes) > 0:
            self.sequence[self.indexes[-1]].previous()
        return self

    def next(self):
        if len(self.indexes) > 0:
            self.sequence[self.indexes[-1]].next()
        return self


class DecimalSequence(Sequence):
    def __init__(self):
        super().__init__('0123456789')


class TwoDecimalSequence(Sequences):
    def __init__(self):
        super().__init__([
            DecimalSequence(),
            DecimalSequence(),
        ])


class ThreeDecimalSequence(Sequences):
    def __init__(self):
        super().__init__([
            DecimalSequence(),
            DecimalSequence(),
            DecimalSequence(),
        ])


class FourDecimalSequence(Sequences):
    def __init__(self):
        super().__init__([
            DecimalSequence(),
            DecimalSequence(),
            DecimalSequence(),
            DecimalSequence(),
        ])


class AlphabeticalSequence(Sequence):
    def __init__(self):
        super().__init__('ABCDEFGHIJKLMNOPQRSTUVWXYZ')


class TwoAlphabeticalSequence(Sequences):
    def __init__(self):
        super().__init__([
            AlphabeticalSequence(),
            AlphabeticalSequence(),
        ])


class ThreeAlphabeticalSequence(Sequences):
    def __init__(self):
        super().__init__([
            AlphabeticalSequence(),
            AlphabeticalSequence(),
            AlphabeticalSequence(),
        ])


class FourAlphabeticalSequence(Sequences):
    def __init__(self):
        super().__init__([
            AlphabeticalSequence(),
            AlphabeticalSequence(),
            AlphabeticalSequence(),
            AlphabeticalSequence(),
        ])


class VowelSequence(Sequence):
    def __init__(self):
        super().__init__('AEIOU')


class TwoVowelSequence(Sequences):
    def __init__(self):
        super().__init__([
            VowelSequence(),
            VowelSequence(),
        ])


class ThreeVowelSequence(Sequences):
    def __init__(self):
        super().__init__([
            VowelSequence(),
            VowelSequence(),
            VowelSequence(),
        ])


class FourVowelSequence(Sequences):
    def __init__(self):
        super().__init__([
            VowelSequence(),
            VowelSequence(),
            VowelSequence(),
            VowelSequence(),
        ])


class HexadecimalSequence(Sequence):
    def __init__(self):
        super().__init__('0123456789ABCDEF')


class TwoHexadecimalSequence(Sequences):
    def __init__(self):
        super().__init__([
            HexadecimalSequence(),
            HexadecimalSequence(),
        ])


class ThreeHexadecimalSequence(Sequences):
    def __init__(self):
        super().__init__([
            HexadecimalSequence(),
            HexadecimalSequence(),
            HexadecimalSequence(),
        ])


class FourHexadecimalSequence(Sequences):
    def __init__(self):
        super().__init__([
            HexadecimalSequence(),
            HexadecimalSequence(),
            HexadecimalSequence(),
            HexadecimalSequence(),
        ])


class DnaSequence(Sequences):
    def __init__(self):
        super().__init__([
            Sequence('ACGT'),
            Sequence('ACGT'),
            Sequence('ACGT'),
        ])


def factory(pattern):
    """
    Creates a sequence pattern using a string consisting of constants and regular expressions to represent the sequence
    of values. To create a sequence with the following pattern (including the constant "2019"):

    A-2019-00
    A-2019-01
    A-2019-02
    A-2019-99
    B-2019-00
    B-2019-01
    B-2019-99
    C-2019-00
    ...
    Z-2019-00
    Z-2019-01
    Z-2019-98
    Z-2019-99

    Just run the following code

    s = factory ("[A-Z];-2019-;[0-9];[0-9]")

    :param pattern: the pattern to create the sequence.
    :return: the instance of the class Sequences.
    """
    if pattern is None:
        return None

    pat = pattern.split(";")
    if len(pat) <= 0:
        return None

    result = Sequences([])
    for x in pat:
        o = list(exrex.generate(x))
        n = len(o)
        if n == 1 and len(o[0]) > 0:
            result.sequence.append(o[0])
        elif n > 1 and len(o[0]) == 1:
            result.sequence.append(Sequence("".join(o)))
        elif n > 1 and len(o[0]) > 1:
            for x in range(len(o[0])):
                aux = []
                for idx in range(len(o)):
                    if o[idx][x] not in aux:
                        aux.append(o[idx][x])
                if len(aux) > 0:
                    result.sequence.append(Sequence("".join(aux)))
    if len(result.sequence) > 0:
        result.build_indexes()
        return result
    return None
