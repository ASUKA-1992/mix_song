from .bert_evaluator import BertEvaluator
from elasticsearch import Elasticsearch

class EvaluateMod:
    def __init__(self,name):
        self.es = Elasticsearch()
        self.evaluator = BertEvaluator()

    def get_after_lyric(self, before_lyric):
        max_score = .0
        after_lyric = ''
        for r in self.__get_after_lyric(before_lyric):
            score = self.evaluate(before_lyric, r)
            if score >= max_score:
                max_score = score
                after_lyric = r[1]
        return after_lyric
        
    def __get_after_lyric(self, before_lyric):
        results = self.es.search(index='lyrics_pair',
                    body={'query':{'match':{'query':before_lyric}}, 'size':10,})
        return [(result['_source']['query'], result['_source']['response'], result["_score"]) for result in results['hits']['hits']]

    #ポイント評価実施
    def evaluate(self, utt, pair):
        return self.evaluator.evaluate(utt, pair[1])
