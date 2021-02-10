import spacy
import os
import sys


def print_versions():
    print(f'Python version : {sys.version:<{10}}')
    print(f'Spacy version  : {spacy.__version__:<{10}}')
    current_dir_path = os.path.dirname(os.path.realpath(os.getcwd()))
    print(f'Current dir : {current_dir_path:.>{15}}')


def print_token_info(spacy_doc):
    """ print_token_info will print for every token of a spacy document
        Text: The original word text.
        Lemma: The base form of the word.
        POS: The simple UPOS part-of-speech tag.
        Tag: The detailed part-of-speech tag.
        Dep: Syntactic dependency, i.e. the relation between tokens.
        Shape: The word shape – capitalization, punctuation, digits.
        is alpha: Is the token an alpha character?
        is stop: Is the token part of a stop list, i.e. the most common words of the language?

    :param spacy_doc: a spacy parsed document
    :return: None
    """
    # https://spacy.io/usage/spacy-101#annotations-pos-deps
    print(f'TEXT       |LEMMA	   |POS    |TAG  |{"TAG explanation":{42}} |DEP        |SHAPE    |ALPHA |STOP')
    print('-'*115)
    for token in spacy_doc:
        print(f'{token.text:{10}} |{token.lemma_:{10}} |{token.pos_:{6}} |{token.tag_:{5}}'
              f'|{spacy.explain(token.tag_):{42}}'
              f' |{token.dep_:{10}} |{token.shape_:{8}} |{token.is_alpha:{5}}|{token.is_stop:{3}}'
              )


def print_token_pos_frequency(spacy_doc):
    pos_counts = doc.count_by(spacy.attrs.POS)
    total_tokens = len(doc)
    for k, v in sorted(pos_counts.items()):
        print(f'{k:{5}}: {doc.vocab[k].text:{5}} = {spacy.explain(doc.vocab[k].text):.<{15}}:'
              f' {v:>{4}} ({v/total_tokens:.2%})')


def print_entities_in_sentence(spacy_doc):
    for i, sentence in enumerate(spacy_doc.sents):
        phrase = nlp(sentence.text)
        if phrase.ents:
            print(f'##### [{i:0>{3}}] ENTITY FOUND IN THIS SENTENCE :')
            displacy.render(phrase, style='ent', jupyter=True)
        else:
            print(f"##### [{i:0>{3}}] NO ENTITY FOUND IN THIS SENTENCE :\n{phrase.text}")


if __name__ == '__main__':
    nlp = spacy.load("en_core_web_sm")
    doc = nlp("Apple is looking at buying U.K. startup for $1 billion !")
    print_token_info(doc)
    print(f'{"PART OF SPEECH (POS) TOKEN FREQUENCY":*^{60}}')
    print_token_pos_frequency(doc)

    print_versions()

