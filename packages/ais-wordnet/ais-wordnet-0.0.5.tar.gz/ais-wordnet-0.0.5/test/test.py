from ais import wordnet
from ais import sentence
test_data = ['phòng','đảng','chính quyền','làm chủ','ban','đảng viên']

sample_wordnet = wordnet.Wordnet('wordnet10-4-2019.xlsx')

#get synset
for each in test_data:
    print(sample.get_ez_synsets_as_row(each))

tag_list = ['n','v','a','e']
sentence = 'thế lực thù địch có những âm mưu gì'

s = sentence.Sentence(sentence,tag_list)
print(s.get_similar_sentences_as_list(sample))