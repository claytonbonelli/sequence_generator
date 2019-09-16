from sequence import ThreeVowelSequence, TwoDecimalSequence, Sequences, Sequence, DnaSequence, factory, DecimalSequence

print("\n3 Vowels")
s = ThreeVowelSequence()
for x in range(100):
    print(s.next().get())

print("\n2 decimals")
s = TwoDecimalSequence()
for x in range(100):
    print(s.next().get())

print("\nCustom")
s = Sequences([
    Sequence('3A4B5X'),
    '-',
    TwoDecimalSequence(),
])
for x in range(500):
    print(s.next().get())

print("\nDNA")
s = Sequences([
    DnaSequence(),
    '-',
    DnaSequence(),
    '-',
    DnaSequence(),
])
while s.next().get() != 'AAA-AAC-GTA':
    print(s.get())
print(s.get())

print("\nPattern with next")
seq = factory(r"WM;-;[0-9];[0-9]")
for x in range(100):
    print(seq.next().get())

print("\nPattern with previous")
seq = factory(r"WM;-;[0-9];[0-9]")
for x in range(100):
    print(seq.previous().get())

print("\nOther pattern")
seq = factory(r"WM-;[0-9]{4}")
for x in range(100):
    print(seq.next().get())
