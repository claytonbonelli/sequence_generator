# Sequence Generator


Number or letter sequences are easy to obtain when you are only interested in sequence of numbers (ascending or descending) that follow
a predefined order, for example decimal numbers 0,1,2,3,4,5,6,7,8,9 always follow that order, the number 1 will follow the number 0, the number 3 will follow the number 2.

Other numbers of larger quantities also follow the same order of formation, ie all are composed of digits between 0 and 9. This same feature for sequential letters can be applied to vowels, all of which correspond to characters sequences that follow a predefined order. 

But, what if you need to create a sequence that has a completely different formation order? A string or number that does not follow the rule natural of decimal numbers or the alphabet? For example, if you need to create sequences like the following:

```pascal
AA-0001
AA-0002
AA-0003

AA-9999
AB-0001
AB-0002
AB-0003

AB-9999
AC-0001
AC-0002
AC-0003

AC-9999
AD-0001
AD-0002
AD-0003


Other sequence

A-2019-01
A-2019-02
A-2019-03

A-2019-99
B-2019-01
B-2019-02

B-2019-99
C-2019-01
C-2019-02
```

How to create growing sequences but made up of characters made up of letters, numbers, punctuation marks, etc.? For this kind of need it is that the "sequence" package was created which contains classes and the means that allow the definition of a sequence of alphanumeric values and the generation these values in ascending / descending sequential order.

You can define any sequence of numeric or alphanumeric characters, which can be letters, numbers, decimals, hexadecimals, DNA sequence, etc. Using the sequence generator you can create sequences that will be generated in ascending or descending order.

You can create your own sequences or use the predefined ones.

Example:

```python
s = Sequences([TwoAlphabeticalSequence(), '-', FourDecimalSequence()])
for x in range(100):
    print(s.get())


s = Sequences([AlphabeticalSequence(), '-', '2019', '-', TwoDecimalSequence()])
for x in range(100):
    print(s.get())


s = Sequences([DnaSequence(), '-', DnaSequence(), '-', DnaSequence()])
while s.next().get() != 'AAA-AAC-GTA':
    print(s.get())
    
print(s.get())
```
