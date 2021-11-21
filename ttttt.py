from pymongo import MongoClient, collection


connection = MongoClient(host='10.2.14.10',port=27017)
db = connection.kingstone
collection = db['cleanbook']
from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger, CkipNerChunker
ws_driver = CkipWordSegmenter(level=3)
pos_driver = CkipPosTagger(level=3)
ner_driver = CkipNerChunker(level=3)
text = list(collection.aggregate([{'$project':{'_id':0,'書籍簡介':1}},{'$sample':{'size':1}}]))[0]['書籍簡介']
# print(text)
ws  = ws_driver(text)
pos = pos_driver(ws)
ner = ner_driver(text)
# Pack word segmentation and part-of-speech results
def pack_ws_pos_sentece(sentence_ws, sentence_pos):
   assert len(sentence_ws) == len(sentence_pos)
   res = []
   for word_ws, word_pos in zip(sentence_ws, sentence_pos):
      res.append(f"{word_ws}({word_pos})")
   return "\u3000".join(res)

# Show results
for sentence, sentence_ws, sentence_pos, sentence_ner in zip(text, ws, pos, ner):
   print(sentence)
   print(pack_ws_pos_sentece(sentence_ws, sentence_pos))
   for entity in sentence_ner:
      print(entity)
   print()