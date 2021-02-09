import spacy
from spacy.matcher import Matcher
from spacy.language import Language
from spacy.tokens import Span
from my_nlp_lib import spacy_utilities as su


if __name__ == '__main__':
    text = """En 1815, M. Charles-François-Bienvenu Myriel était évêque de Digne.
Vrai ou faux, ce qu'on dit des hommes tient de ce qu'ils font. 
M. Myriel était fils d'un conseiller au parlement d'Aix; 
Charles Myriel, nonobstant son mariage avec Mademoiselle Francine Binochoux,
était un homme heureux.
M. Charles Myriel, dès les premiers jours de la
révolution, émigra en Italie. Sa femme y mourut d'une maladie de
poitrine. Que se passa-t-il ensuite dans la destinée de M. Myriel?

En 1804, M. Myriel était curé de Brignolles.
"""

    # load the normal french model
    nlp = spacy.load('fr_core_news_sm')


    @Language.component("expand_person_entities")
    def expand_person_entities(spacy_doc):
        new_ents = []
        for ent in spacy_doc.ents:
            if ent.label_ == "PERSON" and ent.start != 0:
                prev_token = spacy_doc[ent.start - 1]
                if prev_token.text in ("Dr", "Dr.", "M.", "Monsieur", "Mme", "Madame"):
                    new_ent = Span(spacy_doc, ent.start - 1, ent.end, label=ent.label)
                    new_ents.append(new_ent)
            else:
                new_ents.append(ent)
        spacy_doc.ents = new_ents
        return spacy_doc


    # Add the component after the named entity recognizer
    nlp.add_pipe("expand_person_entities", after="ner")

    # matcher = Matcher(nlp.vocab)
    # # Add match ID "HelloWorld" with no callback and one pattern
    # pattern = [{"ORTH": "M."}, {"ORTH": "Myriel"}]
    # matcher.add("MonsieurX", [pattern])
    doc = nlp(text)

    su.print_token_info(doc)

    print('# Now we will try to find the named entities, phrases and concepts')
    for e in doc.ents:
        print(f'{e.text:{25}} {e.label_:{10}} {spacy.explain(e.label_):{40}}')
