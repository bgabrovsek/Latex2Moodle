from moodle import *
import latex as lx
from pathlib import Path
from sympy import *

# vhodne datoteke
input_latex = Path("latex") / "03-poisci-vektor.tex"
proto_cloze = Path("proto") / "proto-cloze.xml"

# preberi latex
d = lx.read(input_latex)



# izpiši osnovne podatke o nalogi
print("   Kategorija:", d['category'])
print("Ime vprašanja:", d['name'])
print("    Parametri:", ','.join(d['params']))
print("       Pogoji:", ' & '.join(d['conditions']))
print("       Random:", d['randomize'])

# dobi parametre in neznanke iz naloge
variables_all = lx.get_all_eval_variables(d['text'])
parameters = d['params']
unused_variables = set(variables_all) - set(parameters)
if len(unused_variables) > 0:
    simboli = symbols(' '.join(unused_variables)) # dodaj simbole (neuporabljene spremenljivke) v tabelo

print("Spremenljivke:",",".join(unused_variables))
print()

#d['n'] = 5

# generiranje nalog
print("Generiranje", d['n'], "vprašanj...")

question_number = 0  # števec nalog
all_question_texts = []

# glavna zanka čez parametre
for vals in lx.loop_through_parameters(d):
    if question_number >= d['n']:
        break
    # leading-zero string števec in izpiši
    qs = "{:03d}".format(question_number)
    print(qs+": ",", ".join( [p+"="+str(val) for p,val in zip(d['params'], vals)]), end="", flush=True) # izpiši parametre

    final_text = ""

    good_exercise = True

    # PREVERI POGOJE

    for pogoj in d['conditions']:
        evaluated = lx.clean_eq(pogoj)
        evaluated = lx.clean_and_insert(evaluated, d['params'], vals)
        evaluated = sympify(evaluated)
        print(evaluated)
        if (not evaluated):
            good_exercise = False
    if not good_exercise:
        print(" (ne zadošča pogoju)")
        continue

    # EVALVIRAJ LATEX


    rezultati = ""

    lat = lx.split_math(d['text'])  # razreži na formule in besedilo
    for tip, subtext in lat:
        if tip >= 1:
            # math mode
            # pojdi čez vse "\eval" tag-e in jih evalviraj
            replacements = []
            for expression in lx.tags(subtext, "eval"):

                evaluated = lx.clean_and_insert(expression, d['params'], vals)
                evaluated = sympify(evaluated)
                replacements.append(("\\eval{"+expression+"}", latex(evaluated))) # add replacements

            # make replacements
            for s1, s2 in replacements:
                subtext = subtext.replace(s1, s2)

            # dodaj evalviran zapis v celotno besedilo
            if tip == 1:
                final_text += "\\(\\displaystyle " + subtext + "\\)"
            if tip == 2:
                final_text += "<p>\\(\\qquad \\displaystyle " + subtext + "\\)</p>"

        else:
            # text mode
            # find and evaluate solutions
            replacements = []
            for expression in lx.tags(subtext, "solution"):
                evaluated = lx.clean_and_insert(expression, d['params'], vals)
                print(evaluated)
                evaluated = sympify(evaluated)

                numerical_result = N(evaluated, 4)

                #if abs(numerical_result) < 0.02:
                #    good_exercise = False

                rezultati += str(numerical_result) + " "
                print("numerical result", numerical_result)
                cloze_string = "{1:NUMERICAL:=" + str(numerical_result) + ":0.1}"
                replacements.append(("\\solution{"+expression+"}", cloze_string))  # add replacements

            for s1, s2 in replacements:
                subtext = subtext.replace(s1, s2)

            final_text += subtext

    if good_exercise:
        all_question_texts.append(final_text)
        question_number += 1
    #if question_number % 10 == 0: print('.', end="", flush=True)


    print("; Rezultat:", rezultati+ ("(ok)" if good_exercise else "(skip)"))

write_xml(proto_cloze, d, all_question_texts)


