import spacy
from spacy.matcher import Matcher
from spacy.language import Language
from spacy.tokens import Span
from my_nlp_lib import spacy_utilities as su


if __name__ == '__main__':
    text = """En 1815, M. Charles-François-Bienvenu Myriel était évêque de Digne.
Vrai ou faux, ce qu'on dit des hommes tient pour l'essentiel de ce qu'ils font. 
M. Myriel était fils d'un conseiller au parlement d'Aix s'appelant Gérard Myriel; 
Charles Myriel, nonobstant son mariage avec Mademoiselle Francine Binochoux,
était un homme heureux. M. Charles Myriel, dès les premiers jours de la révolution, émigra en Italie.
Mme Francine y mourut d'une maladie de poitrine.
Que se passa-t-il ensuite dans la destinée de M. Myriel?
Fut-il pris d'un terrible désespoir, la lumière du Seigneur lui fut-elle révélée ? Nul ne le sait. 
Toujours est-il qu'en 1804, M. Myriel était devenu le curé de Brignoles.
"""

    # load the normal french model
    nlp = spacy.load('fr_core_news_sm')
    doc = nlp(text)
    su.print_token_info(doc)
    print('#'*80)
    print('####List of named entities')
    for e in doc.ents:
        print(f'{e.text:{25}} {e.label_:{10}} {spacy.explain(e.label_):{40}}')
    print('#' * 80)
    print('####ERRORS in the list of named entities:')
    print("""   - Vrai is obviously not a location
    - Fut is also not a location
    - Myriel is a person and not a location
M. it's not a person but should be used as an indicator that next token could be a person
    """)
    ruler = nlp.add_pipe("entity_ruler", before='ner')
    patterns = [{"label": "PER", "pattern": "M. Myriel"},
                {"label": "PER", "pattern": [{"LOWER": "mademoiselle"}, {"LOWER": "Baptistine"}]}]
    ruler.add_patterns(patterns)
    doc = nlp(text)
    print('#' * 80)
    print('####List of named entities')
    for e in doc.ents:
        print(f'{e.text:{25}} {e.label_:{10}} {spacy.explain(e.label_):{40}}')
    print('#' * 80)
