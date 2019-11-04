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
        :return: self
        """
        return self

    def last(self):
        """
        Advance to the last sequence.
        :return: self
        """
        self.index = len(self.sequence) - 1
        return self

    def first(self):
        """
        Return to the first sequence.
        :return: self
        """
        self.index = 0
        return self

    def send_to_parent(self, *args, **kwargs):
        """
        Send a message for the parent.
        :return: self
        """
        if self.parent:
            self.parent.send(self, *args, **kwargs)
        return self

    def set(self, value):
        """
        Set the current sequence.
        :param value: the next sequence.
        :return: self
        """
        old = self.get()
        if old == value:
            return self
        while True:
            v = self.next().get()
            if v == value:
                return self
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

    RIGHT_TO_LEFT = 0
    LEFT_TO_RIGHT = 1

    def __init__(self, sequence, parent=None, direction=RIGHT_TO_LEFT, order=None):
        super().__init__(sequence, parent)
        self.indexes = []
        self.build_indexes()
        self.direction = direction
        self.order = order
        self.check_order()

    def check_order(self):
        if self.sequence is None or len(self.sequence) <= 0:
            return
        if self.order is None or len(self.order) <= 0:
            return
        for o in self.order:
            seq = self.sequence[o]
            if not isinstance(seq, Sequence):
                raise Exception('order at [{index}] is not a Sequence, please use only the indexes {values}'.format(
                    index=o, values=self.indexes,
                ))

    def get_sequences(self):
        """
        :return: all sequences from this sequence.
        """
        def inner(seq, result=[]):
            if isinstance(seq, Sequences):
                for s in seq.sequence:
                    inner(s, result)
            elif isinstance(seq, Sequence):
                if len(seq.sequence.strip()) > 1:
                    result.append({
                        "sequence": seq.sequence,
                        "index": seq.index,
                    })
            return result
        return inner(self, [])

    def size(self):
        """
        :return: the number of sequences possibles to generate.
        """
        sequences = self.get_sequences()
        if sequences is None or len(sequences) <= 0:
            return 0
        result = 1
        for seq in sequences:
            result *= len(seq['sequence'])
        return result

    def distance_to_last(self):
        """
        :return: the distance from the current sequence to the last sequence.
        """
        result = 0
        sequences = self.get_sequences()
        n = len(sequences)
        if sequences is None or n <= 0:
            return 0
        for i, v in enumerate(sequences):
            index = v['index']
            if index < 0:
                index = 0
            offset = len(v['sequence']) - index - 1
            if i < (n - 1):
                r = offset
                for k in range((i + 1), n):
                    r *= len(sequences[k]['sequence'])
                result += r
            else:
                result += offset
        return result

    def last(self):
        """
        Advance to the last sequence.
        :return: self
        """
        self.index = len(self.sequence) - 1
        for index, idx in enumerate(self.indexes):
            self.sequence[idx].last()
        return self

    def first(self):
        """
        Return to the first sequence.
        :return: self
        """
        self.index = 0
        for index, idx in enumerate(self.indexes):
            self.sequence[idx].first()
        return self

    def build_indexes(self):
        if self.sequence is None or len(self.sequence) <= 0:
            return
        for index, value in enumerate(self.sequence):
            if not isinstance(value, Sequence):
                continue
            value.parent = self
            self.indexes.append(index)

    def _index_of(self, sequence, indexes):
        for index, idx in enumerate(indexes):
            if self.sequence[idx] == sequence:
                return index
        return None

    def send(self, *args, **kwargs):
        """
        Send a message to this class.
        :return: self
        """
        size = len(self.indexes)
        if size <= 0:
            return self

        flow = kwargs.get('flow')
        sequence = args[0]

        method_name = "next" if flow == self.OVERFLOW else "previous"
        index = self._index_of(sequence, self.indexes)

        if self.order and len(self.order) > 0:
            index = self._index_of(sequence, self.order)
            if index < (len(self.order) - 1):
                sequence = self.sequence[self.order[index + 1]]
                getattr(sequence, method_name)()
                return self
        elif self.direction == self.RIGHT_TO_LEFT:
            if index > 0:
                sequence = self.sequence[self.indexes[index - 1]]
                getattr(sequence, method_name)()
                return self
        elif self.direction == self.LEFT_TO_RIGHT:
            if index < (len(self.indexes) - 1):
                sequence = self.sequence[self.indexes[index + 1]]
                getattr(sequence, method_name)()
                return self
        self.send_to_parent(flow=flow)
        return self

    def get(self):
        """
        :return: the current sequence's value.
        """
        result = ''
        for value in self.sequence:
            if isinstance(value, Sequence):
                result += str(value.get())
            else:
                result += value
        return result

    def previous(self):
        """
        Return to the previous sequence.
        :return: self
        """
        if len(self.indexes) > 0:
            self._get_sequence_to_advance().previous()
        return self

    def _get_sequence_to_advance(self):
        if self.order and len(self.order) > 0:
            return self.sequence[self.order[0]]
        elif self.direction == self.RIGHT_TO_LEFT:
            return self.sequence[self.indexes[-1]]
        elif self.direction == self.LEFT_TO_RIGHT:
            return self.sequence[self.indexes[0]]
        return None

    def next(self):
        """
        Advance to the next sequence.
        :return: self
        """
        if len(self.indexes) > 0:
            self._get_sequence_to_advance().next()
        return self


def factory(pattern, first_value=None, direction=Sequences.RIGHT_TO_LEFT, order=None):
    """
    Creates a sequence pattern using a string consisting of constants and regular expressions to represent the sequence
    of values.

    :param pattern: the pattern to create the sequence.
    :param first_value: the first value of the sequence.
    :param direction: the direction of the sequence.
    :param order: the sequence growth order.
    :return: the instance of the class Sequences.

    Examples: the following snippets will generate the sequences:

    s = factory ("[A-Z]-2019-[0-9][0-9]")
    for x in range(300):
        print(s.next().get())

    A-2019-00
    A-2019-01
    A-2019-02
    ...
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

    s = factory ("[A-Z]-2019-[0-9][0-9]", direction=Sequences.LEFT_TO_RIGHT)
    for x in range(300):
        print(s.next().get())

    A-2019-00
    B-2019-00
    C-2019-00
    D-2019-00
    E-2019-00
    ...
    X-2019-00
    Y-2019-00
    Z-2019-00
    A-2019-10
    B-2019-10
    C-2019-10
    ...
    X-2019-10
    Y-2019-10
    Z-2019-10
    A-2019-20
    B-2019-20
    C-2019-20
    ...
    X-2019-90
    Y-2019-90
    Z-2019-90
    A-2019-01
    B-2019-01
    C-2019-01

    s = factory("[A-Z]-2019-[0-9][0-9]", order=[8, 0, 7])
    for x in range(300):
        print(s.next().get())

    A-2019-00
    A-2019-01
    A-2019-02
    A-2019-03
    A-2019-04
    A-2019-05
    A-2019-06
    A-2019-07
    A-2019-08
    A-2019-09
    B-2019-00
    B-2019-01
    B-2019-02
    B-2019-03
    B-2019-04
    ...
    Z-2019-07
    Z-2019-08
    Z-2019-09
    A-2019-10
    A-2019-11
    A-2019-12
    A-2019-13
    A-2019-14

    """
    if pattern is None:
        return None

    pat = pattern.split(";")
    if len(pat) <= 0:
        return None

    result = Sequences([], direction=direction, order=order)
    for x in pat:
        o = list(exrex.generate(x))
        n = len(o)
        if n == 1 and len(o[0]) > 0:
            result.sequence.append(o[0])
        elif n > 1 and len(o[0]) == 1:
            result.sequence.append(Sequence("".join(o)))
        elif n > 1 and len(o[0]) > 1:
            for y in range(len(o[0])):
                aux = []
                for idx in range(len(o)):
                    if o[idx][y] not in aux:
                        aux.append(o[idx][y])
                if len(aux) > 0:
                    if len(aux) > 1:
                        result.sequence.append(Sequence("".join(aux)))
                    else:
                        result.sequence.append(aux[0])
    if len(result.sequence) <= 0:
        return None

    result.build_indexes()

    if order and len(order) > 0:
        result.check_order()

    if first_value is not None:
        result.set(first_value)

    return result
