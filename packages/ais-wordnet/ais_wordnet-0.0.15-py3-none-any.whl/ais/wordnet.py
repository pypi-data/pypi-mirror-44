import logging
from pandas import ExcelFile,read_excel

class Wordnet:    
    def __init__(self,wordnet_path):
        logger = logging.getLogger(__name__)
        logger.info("initing Wordnet object")
        logger.info('current path: ', wordnet_path = wordnet_path if wordnet_path else 'not specified yet')
        self.wordnet = None
        self.default_index = 0
        if wordnet_path:
            self.wordnet = ExcelFile(wordnet_path)
    
    '''
        @params:
                what_to_search: input a word
                category: từ loại
        return : mảng 2 chiều các từ đồng nghĩa 

    '''
    def get_ez_synsets_as_row(self,what_to_search,category="n"):
        default_sheet = read_excel(self.wordnet,category,header = None, na_values = "", keep_default_na = False).fillna('')
        unfiltered_results = default_sheet[default_sheet[self.default_index] == what_to_search].values.tolist()
        results = []
        if len(unfiltered_results) > 0:
            for each in unfiltered_results[0]:
                if each != '':
                    results.append(each)
        else:
            results.append(what_to_search)
        return results

  