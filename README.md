# sequence_generator
Generate sequences of numbers and/or characters

# See example.py

You can define any sequence of numeric or alphanumeric characters, which can be letters, numbers, decimals, hexadecimals, DNA sequence, etc.
Using the sequence generator you can create sequences that will be generated in ascending or descending order.
You can create your own sequences or use the predefined ones.

```python
s = Sequences([DnaSequence(), '-', DnaSequence(), '-', DnaSequence()])
while s.next().get() != 'AAA-AAC-GTA':
    print(s.get())
print(s.get())
```
