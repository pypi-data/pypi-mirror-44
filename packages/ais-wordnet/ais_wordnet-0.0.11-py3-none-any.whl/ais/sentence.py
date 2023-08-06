import logging
import itertools
from underthesea import pos_tag


class Sentence:
    def __init__(self,sample_sentence="",tag_list=[]):
        logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
        logger = logging.getLogger(__name__)
        logger.info('initing sentence object')
        self.sample_sentence = sample_sentence
        self.tag_list = tag_list

    def get_similar_sentences_as_words(self,wordnet):
        tokenized_sentence = pos_tag(self.sample_sentence)
        multiple_choice = []
        for each in tokenized_sentence:
            if each[1] in self.tag_list:
                multiple_choice.append(wordnet.get_ez_synsets_as_row(each[0],each[1].lower()))
            else:
                multiple_choice.append(wordnet.get_ez_synsets_as_row(each[0]))
        
        out = list(itertools.product(*multiple_choice))
        return out
    
    def get_similar_sentences_as_list(self,wordnet):
        out = self.get_similar_sentences_as_words(wordnet)
        for i in range (0,len(out)):
            out[i] = ' '.join(out[i])
        return out

    
    
    def get_similar_sentence_with_score(self,wordnet,doc2vecmodel):
        pass