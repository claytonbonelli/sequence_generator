import unittest
from sequence import factory, Sequences


class MyTestCase(unittest.TestCase):

    def test_factory(self):
        seq = factory("[ABC]{2} [0-9]{2}")
        self.assertEqual(type(seq), Sequences)

    def test_order_is_plain(self):
        seq = factory("[ABC]{2} [0-9]{2}", order=[1, 0, 4, 3])
        self.assertEqual(seq.order, [1, 0, 4, 3])

        seq = factory("[ABC]{2} [0-9]{2}", order=[[1, 0, 4, 3]])
        self.assertEqual(seq.order, [1, 0, 4, 3])

        seq = factory("[ABC]{2} [0-9]{2}", order=[[[[[[1, 0, 4, 3]]]]]])
        self.assertEqual(seq.order, [1, 0, 4, 3])

        seq = factory("[ABC]{2} [0-9]{2}", order=[[1, 0], [4, 3]])
        self.assertEqual(seq.order, [1, 0, 4, 3])

        seq = factory("[ABC]{2} [0-9]{2}", order=[[1, [0]], [4], [3]])
        self.assertEqual(seq.order, [1, 0, 4, 3])

    def test_get_sequences(self):
        seq = factory("[ABC]{2} [0-9]{2}")
        sequences = seq.get_sequences()
        self.assertEqual(len(sequences), 4)
        self.assertEqual(sequences[0]['sequence'], 'ABC')
        self.assertEqual(sequences[1]['sequence'], 'ABC')
        self.assertEqual(sequences[2]['sequence'], '0123456789')
        self.assertEqual(sequences[3]['sequence'], '0123456789')

    def test_size(self):
        seq = factory("[ABC]{2} [0-9]{2}")
        self.assertEqual(seq.size(), 900)

        seq = factory("[ABC]{2} [0-9]{2}", direction=Sequences.LEFT_TO_RIGHT)
        self.assertEqual(seq.size(), 900)

        seq = factory("[ABC]{2} [0-9]{2}", order=[1, 0, 4, 3])
        self.assertEqual(seq.size(), 900)

    def test_last(self):
        seq = factory("[ABC]{2} [0-9]{2}")
        self.assertEqual(seq.last().get(), 'CC 99')

        seq = factory("[ABC]{2} [0-9]{2}", direction=Sequences.LEFT_TO_RIGHT)
        self.assertEqual(seq.last().get(), 'CC 99')

        seq = factory("[ABC]{2} [0-9]{2}", order=[1, 0, 4, 3])
        self.assertEqual(seq.last().get(), 'CC 99')

        for x in range(10):
            seq.next()
        self.assertEqual(seq.last().get(), 'CC 99')

    def test_first(self):
        seq = factory("[ABC]{2} [0-9]{2}")
        self.assertEqual(seq.first().get(), 'AA 00')

        seq = factory("[ABC]{2} [0-9]{2}", direction=Sequences.LEFT_TO_RIGHT)
        self.assertEqual(seq.first().get(), 'AA 00')

        seq = factory("[ABC]{2} [0-9]{2}", order=[1, 0, 4, 3])
        self.assertEqual(seq.first().get(), 'AA 00')

        for x in range(10):
            seq.next()
        self.assertEqual(seq.first().get(), 'AA 00')

    def test_build_indexes(self):
        seq = factory("[ABC]{2} [0-9]{2}")
        seq.build_indexes()
        self.assertEqual(seq.indexes, [0, 1, 3, 4])

    def test_next(self):
        seq = factory("[ABC]{2} [0-9]{2}")
        self.assertEqual(seq.next().get(), 'AA 00')
        self.assertEqual(seq.next().get(), 'AA 01')
        self.assertEqual(seq.next().get(), 'AA 02')
        self.assertEqual(seq.next().get(), 'AA 03')
        self.assertEqual(seq.next().get(), 'AA 04')
        self.assertEqual(seq.next().get(), 'AA 05')
        self.assertEqual(seq.next().get(), 'AA 06')
        self.assertEqual(seq.next().get(), 'AA 07')
        self.assertEqual(seq.next().get(), 'AA 08')
        self.assertEqual(seq.next().get(), 'AA 09')
        self.assertEqual(seq.next().get(), 'AA 10')

        seq = factory("[ABC]{2} [0-9]{2}", direction=Sequences.LEFT_TO_RIGHT)
        self.assertEqual(seq.next().get(), 'AA 00')
        self.assertEqual(seq.next().get(), 'BA 00')
        self.assertEqual(seq.next().get(), 'CA 00')
        self.assertEqual(seq.next().get(), 'AB 00')
        self.assertEqual(seq.next().get(), 'BB 00')
        self.assertEqual(seq.next().get(), 'CB 00')
        self.assertEqual(seq.next().get(), 'AC 00')
        self.assertEqual(seq.next().get(), 'BC 00')
        self.assertEqual(seq.next().get(), 'CC 00')
        self.assertEqual(seq.next().get(), 'AA 10')

        seq = factory("[ABC]{2} [0-9]{2}", order=[1, 0, 4, 3])
        self.assertEqual(seq.next().get(), 'AA 00')
        self.assertEqual(seq.next().get(), 'AB 00')
        self.assertEqual(seq.next().get(), 'AC 00')
        self.assertEqual(seq.next().get(), 'BA 00')
        self.assertEqual(seq.next().get(), 'BB 00')
        self.assertEqual(seq.next().get(), 'BC 00')
        self.assertEqual(seq.next().get(), 'CA 00')
        self.assertEqual(seq.next().get(), 'CB 00')
        self.assertEqual(seq.next().get(), 'CC 00')
        self.assertEqual(seq.next().get(), 'AA 01')
        self.assertEqual(seq.next().get(), 'AB 01')
        self.assertEqual(seq.next().get(), 'AC 01')

    def test_previous(self):
        seq = factory("[ABC]{2} [0-9]{2}")
        self.assertEqual(seq.next().get(), 'AA 00')
        self.assertEqual(seq.previous().get(), 'CC 99')
        self.assertEqual(seq.previous().get(), 'CC 98')
        self.assertEqual(seq.previous().get(), 'CC 97')
        self.assertEqual(seq.previous().get(), 'CC 96')
        self.assertEqual(seq.previous().get(), 'CC 95')
        self.assertEqual(seq.previous().get(), 'CC 94')
        self.assertEqual(seq.previous().get(), 'CC 93')
        self.assertEqual(seq.previous().get(), 'CC 92')
        self.assertEqual(seq.previous().get(), 'CC 91')
        self.assertEqual(seq.previous().get(), 'CC 90')
        self.assertEqual(seq.previous().get(), 'CC 89')

        seq = factory("[ABC]{2} [0-9]{2}", direction=Sequences.LEFT_TO_RIGHT)
        self.assertEqual(seq.next().get(), 'AA 00')
        self.assertEqual(seq.next().get(), 'BA 00')
        self.assertEqual(seq.next().get(), 'CA 00')
        self.assertEqual(seq.next().get(), 'AB 00')
        self.assertEqual(seq.next().get(), 'BB 00')
        self.assertEqual(seq.previous().get(), 'AB 00')
        self.assertEqual(seq.previous().get(), 'CA 00')
        self.assertEqual(seq.previous().get(), 'BA 00')
        self.assertEqual(seq.previous().get(), 'AA 00')
        self.assertEqual(seq.previous().get(), 'CC 99')
        self.assertEqual(seq.previous().get(), 'BC 99')

        seq = factory("[ABC]{2} [0-9]{2}", order=[1, 0, 4, 3])
        self.assertEqual(seq.next().get(), 'AA 00')
        self.assertEqual(seq.next().get(), 'AB 00')
        self.assertEqual(seq.next().get(), 'AC 00')
        self.assertEqual(seq.next().get(), 'BA 00')
        self.assertEqual(seq.next().get(), 'BB 00')
        self.assertEqual(seq.next().get(), 'BC 00')
        self.assertEqual(seq.previous().get(), 'BB 00')
        self.assertEqual(seq.previous().get(), 'BA 00')
        self.assertEqual(seq.previous().get(), 'AC 00')
        self.assertEqual(seq.previous().get(), 'AB 00')
        self.assertEqual(seq.previous().get(), 'AA 00')
        self.assertEqual(seq.previous().get(), 'CC 99')
        self.assertEqual(seq.previous().get(), 'CB 99')
        self.assertEqual(seq.previous().get(), 'CA 99')
        self.assertEqual(seq.previous().get(), 'BC 99')
        self.assertEqual(seq.previous().get(), 'BB 99')
        self.assertEqual(seq.previous().get(), 'BA 99')
        self.assertEqual(seq.previous().get(), 'AC 99')
        self.assertEqual(seq.previous().get(), 'AB 99')
        self.assertEqual(seq.previous().get(), 'AA 99')
        self.assertEqual(seq.previous().get(), 'CC 98')
        self.assertEqual(seq.previous().get(), 'CB 98')


if __name__ == '__main__':
    unittest.main()
