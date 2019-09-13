class Sequence:
    def __init__(self, sequence, parent=None):
        self.sequence = sequence
        self.index = -1
        self.parent = parent

    def send(self, *args, **kwargs):
        raise NotImplemented()

    def send_to_parent(self):
        if self.parent:
            self.parent.send(self)

    def set(self, value):
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
        if self.index == -1:
            self.index = 0
        return self.sequence[self.index]

    def next(self):
        self.index += 1
        if self.index < len(self.sequence):
            return self

        # Overflow
        self.index = 0
        self.send_to_parent()
        return self


class Sequences(Sequence):
    def __init__(self, sequence, parent=None):
        super().__init__(sequence, parent)
        self.indexes = []
        for index, value in enumerate(self.sequence):
            if not isinstance(value, Sequence):
                continue
            value.parent = self
            self.indexes.append(index)

    def send(self, *args, **kwargs):
        if len(self.indexes) <= 0:
            return

        sequence = args[0]
        for index, idx in enumerate(self.indexes):
            if self.sequence[idx] != sequence:
                continue

            if index > 0:
                self.sequence[self.indexes[index - 1]].next()
                return

            # index == 0
            self.send_to_parent()
            return

    def get(self):
        result = ''
        for value in self.sequence:
            if isinstance(value, Sequence):
                result += str(value.get())
            else:
                result += value
        return result

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
