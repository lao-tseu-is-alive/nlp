import sys
import numpy as np
import spacy


def py_version(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Python version : {sys.version}')  # Press Ctrl+F8 to toggle the breakpoint.
    print(f'Numpy  version : {spacy.__version__}')  # Press Ctrl+F8 to toggle the breakpoint.
    print(f'Spacy  version : {spacy.__version__}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    py_version('PyCharm')

    # Load English tokenizer, tagger, parser and NER
    nlp = spacy.load("en_core_web_sm")

    # Process whole documents like this speech from Martin Luther King 'I Have a Dream' back in 1963
    text = ("""
    I have a dream that one day down in Alabama, with its vicious racists, 
    with its governor having his lips dripping with the words of interposition and nullification 
    – one day right there in Alabama little black boys and black girls will be able to join hands 
    with little white boys and white girls as sisters and brothers.
    I have a dream today.
    """)
    doc = nlp(text)

    print('## Let us try to analyze syntax:')
    print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
    print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

    print('# Now we will try to find the named entities, phrases and concepts')
    for entity in doc.ents:
        print(entity.text, entity.label_)
