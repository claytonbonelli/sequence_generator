from sequence import ThreeVowelSequence, TwoDecimalSequence, Sequences, Sequence, DnaSequence

print("3 Vowels")
s = ThreeVowelSequence()
for x in range(100):
    print(s.next().get())

print("2 decimals")
s = TwoDecimalSequence()
for x in range(100):
    print(s.next().get())

print("Custom")
s = Sequences([
    Sequence('3A4B5X'),
    '-',
    TwoDecimalSequence(),
])
for x in range(500):
    print(s.next().get())

print("DNA")
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

