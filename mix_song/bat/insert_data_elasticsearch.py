from elasticsearch import Elasticsearch, helpers
es = Elasticsearch()

print('読み込みファイル名')
file_name = input('>> ')

def load():
    with open('../tmp/' + file_name, encoding="utf8", errors='ignore') as f:
        for i, __ in enumerate(f):
            print(i, '...', end='\r')
            __ = __.split('\t')
            before = __[0].strip()
            print(before)
            after = __[1].strip()
            print(after)
            item = {'_index':'lyrics_pair', '_type':'docs', '_source':{ 'query':before, 'response':after }}
            yield item

if __name__ == '__main__':
    print(helpers.bulk(es, load()))
