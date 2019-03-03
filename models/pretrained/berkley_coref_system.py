from allennlp.data.dataset_readers.dataset_utils.ontonotes import Ontonotes

from ..heuristics.coref import Coref
from ..heuristics.stanford_base import StanfordModel

class BCS(Coref, StanfordModel):
    def __init__(self, model):
        self.model = model
        super().__init__(model)
        
    def predict(self, text, a, b, pronoun_offset, a_offset, b_offset, id=None, debug=False, **kwargs):
        doc, tokens_, pronoun_offset, a_offset, b_offset, a_span, b_span, pronoun_token, a_tokens, b_tokens = self.tokenize(text, 
                                                                                                        a, 
                                                                                                        b, 
                                                                                                        pronoun_offset, 
                                                                                                        a_offset, 
                                                                                                        b_offset, 
                                                                                                        **kwargs)
        
        data = Ontonotes().dataset_document_iterator('tmp/coref/{}-0.pred_conll'.format(id))
        for i, doc in enumerate(data):
            tokens = []
            clusters = defaultdict(list)
            for fi in doc:
                for c in fi.coref_spans:
                    clusters[c[0]].append([len(tokens)+c[1][0], len(tokens)+c[1][1]])
                tokens += fi.words
                
        tokens = [token.replace('\\*', '*').replace('-LRB-', '(').replace('-RRB-', ')') for token in tokens]
        
        if any([token not in tokens for token in tokens_[a_span[0]:a_span[1]]+tokens_[b_span[0]:b_span[1]]]):
            print('Tokens dont match', tokens, tokens_, a, b)

        return tokens, list(clusters.values()), pronoun_offset, a_span, b_span