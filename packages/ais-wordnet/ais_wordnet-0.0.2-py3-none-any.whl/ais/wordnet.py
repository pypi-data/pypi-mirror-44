import logging
from pandas import ExcelFile,read_excel

class Wordnet:    
    def __init__(self,wordnet_path):
        logging.info("initing Wordnet object")
        logging.info('current path: ', wordnet_path = wordnet_path if wordnet_path else 'not specified yet')
        self.wordnet = None
        self.default_index = 0
        if wordnet_path:
            self.wordnet = ExcelFile(wordnet_path)
        
    def get_ez_synsets_as_row(self,what_to_search,category="n"):
        default_sheet = read_excel(self.wordnet,category,header = None, na_values = "", keep_default_na = False).fillna('')
        results = default_sheet[default_sheet[self.default_index] == what_to_search].values.tolist()
        new = []
        if len(results) > 0:
            for each in results[0]:
                if each != '':
                    new.append(each)

        return new

    def get_more_synsets(self,what_to_search):
        results = []
        if has_subnet(self):            
            for each in self.wordnet.sheet_names:
                sheet = read_excel(self.wordnet,each)
                result.append(get_ez_synsets_as_row(self,what_to_search,each))
        else:
            result.sappend(et_ez_synsets_as_row(self,what_to_search))
        return results 

    def has_subnet(self):
        if len(self.wordnet.sheet_names) > 1:
            return True
    
    def list_subnet(self):
        if has_subnet(self):
            return self.wordnet.sheet_names
        else:
            return []