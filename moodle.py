import codecs
from copy import deepcopy
from pathlib import Path
# global variables
f = None
counter = 0

def moodlify(s):
    while "  " in s:
        s = s.replace("  ", " ")
    repl = [
        ('"c', 'č'), ('"C', 'Č'), ('"s', 'š'), ('"S', 'Š'), ('"z', 'ž'), ('"Z', 'Ž'),
        ('\\v{c}', 'č'), ('\\v{C}', 'Č'), ('\\v{s}', 'š'), ('\\v{S}', 'Š'), ('\\v{z}', 'ž'), ('\\v{Z}', 'Ž'),
        ('\\v c', 'č'), ('\\v C', 'Č'), ('\\v s', 'š'), ('\\v S', 'Š'), ('\\v z', 'ž'), ('\\v Z', 'Ž'),
    ]

    repl_alt = [
        ('$$', ('\\(', '\\)')),
        ('$', ('\\(', '\\)')),
    ]

    for a, b in repl:
        while a in s:
            s = s.replace(a,b)

    for a, (b1, b2) in repl_alt:
        while a in s:
            s = s.replace(a, b1,1)
            s = s.replace(a, b2,1)

    return s


def lines2breaks(s):
    ss = s.split("\n")
    ss = [v.strip() for v in ss]
    ss = [v for v in ss if len(v) > 1 and v[0] != "%" and "newpage" not in v]
    return "<br>".join(ss)


def glava_input(filename):
    global f
    full_filename = filename

    print(full_filename)
    f = codecs.open(full_filename, mode="w", encoding="utf-8")

    # KATEGORIJA
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<quiz>\n')



def noga():
    global f
    f.write('\n</quiz>\n')
    f.close()
    print("Generiranih " + str( counter)+ " vprašanj.")



def dollars_to_moodle(besedilo):
    for x in range(100):
        besedilo = besedilo.replace("$$", "\\[", 1)
        besedilo = besedilo.replace("$$", "\\]", 1)

    for x in range(1000):
        besedilo = besedilo.replace("$","\\(",1)
        besedilo = besedilo.replace("$","\\)",1)
    return besedilo

def non_alphanum_to_dashes(s):
    for i in range(len(s)):
        if not s[i].isalnum():
            s = s[:i] + "-" + s[i+1:]
    return s

def write_xml(proto_filename, d, texts):

    global f

    output_filename = Path('export-xml') / (non_alphanum_to_dashes(d['category']) + ".xml")

    print("Zapis v", output_filename)

    with open(proto_filename, 'r',encoding="utf-8") as fproto:
        proto = fproto.read()



    glava_input(output_filename)

    counter = 0

    for index, text in enumerate(texts):

        text = text.replace("\\\\", "<br>")
        text = lines2breaks(text)

        besedilo = deepcopy(proto)

        besedilo = besedilo.replace("[KATEGORIJA]", d['category'])
        besedilo = besedilo.replace("[IME]", "{:03d}".format(index) +" "+ d['name'])
        besedilo = besedilo.replace("[BESEDILO]", text)

        f.write(besedilo)
        f.write("\n\n")

        counter += 1

    noga()

    print("Zapisanih",counter, "nalog.")