import pytest

from src.sequence import factory, Sequences


class TestAgroceres:
    """
    DN = Data de nascimento
    DNM = Data de nascimento baseado no calendário de mil dias
    R = Raça - letra ou numero
    OP = Ordem de parto - letra ou numero
    OL = Ordem do leitão - letra ou numero
    SEQN = Numero Sequencial numérico
    """

    @pytest.mark.skip(reason="information only")
    def test_sequence(self):
        seq = factory("CHARLES [AEIOU]{2} [\\d]{2} 2019 [a-f]{2}", first_value='CHARLES AA 06 2019 af')

        for x in range(10000):
            print(seq.next().get())

        print("************")
        print(seq.get())
        print(seq.get())
        print(seq.get())

        print("************")
        print(seq.previous().get())
        print(seq.previous().get())
        print(seq.previous().get())

        print(seq.last().get())
        print(seq.first().get())

        assert 1==1

    def test_sequence_1(self):
        """
        SEQN[0001-1599]{4}
        """
        sequence = factory("[0-9]{4}").set('0000')

        sequences = [sequence.next().get() for x in range(1599)]

        assert len(sequences) == 1599

    def test_sequence_2(self):
        """
        DNM[000-999]{3}R[A-Z0-9]{1}OP[A-Z0-9]{1}OL[A-Z0-9]{1}
        """
        sequence = factory("[0-9]{3}[A-Z][A-Z][A-Z]")

        sequences = [sequence.next().get() for x in range(46656)]

        for i in sequences:
            print(i)

        assert len(sequences) == 1599