file = 'C:\\Users\\bostj\\Dropbox\\Code\\2021-Izpit-PSIM-2.tex'

repl = [
    ('"c','č'),('"C','Č'),('"s','š'),('"S','Š'),('"z','ž'),('"Z','Ž'),
    ('\\v{c}','č'),('\\v{C}','Č'),('\\v{s}','š'),('\\v{S}','Š'),('\\v{z}','ž'),('\\v{Z}','Ž'),
    ('\\v c','č'),('\\v C','Č'),('\\v s','š'),('\\v S','Š'),('\\v z','ž'),('\\v Z','Ž'),
    ]

repl_alt = [
    ('$$',('\\(','\\)')),
    ('$' ,('\\(','\\)')),
]

with open(file, 'r',encoding="utf-8") as f:
    text = f.read()

for a, b in repl:
    text = text.replace(a, b)


for a, seq in repl_alt:
    print(a,seq)
    m = 0
    while True:
        i = text.find(a)

        if i >= 0:
            text = text[:i] + seq[m ] + text[i+len(a):]
            m = (m + 1)% len(seq)
        else:
            break

with open(file.replace('.tex','-1.tex'),'w',encoding="utf-8") as f:
    f.write(text)
    print("write")

print("OK.")