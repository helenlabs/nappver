import pysolr

# Setup a Solr instance. The timeout is optional.
solr = pysolr.Solr('http://localhost:8983/solr/solrBoard', timeout=10)
#solr = pysolr.Solr('http://localhost:8983', timeout=10)

# How you'd index data.
solr.add([
    {
        "id": "doc_1",
        "app_name": "테스트 어플리케이션",
        "description": "이 어플리케이션은 졸라 훌륭합니다."
    },
    {
        "id": "doc_2",
        "app_name": "월넛트리 언어게임",
        "description": "최고의 인공지능 어플리케이션!!"
    },
    {
        "id": "doc_3",
        "app_name": "adfsdf asdgafdgd",
        "description": "ser tghsth sdgdrth!!"
    }
], commit=True)



# Note that the add method has commit=True by default, so this is
# immediately committed to your index.

# Later, searching is easy. In the simple case, just a plain Lucene-style
# query is fine.
results = solr.search("app_name:어플리케이션 OR description:어플리케이션")

# The ``Results`` object stores total results found, by default the top
# ten most relevant results and any additional data like
# facets/highlighting/spelling/etc.
print("Saw {0} result(s).".format(len(results)))

# Just loop over it to access the results.
for result in results:
    print("The app_name is '{0}'.".format(result['app_name']))



results = solr.search('테스트')

# The ``Results`` object stores total results found, by default the top
# ten most relevant results and any additional data like
# facets/highlighting/spelling/etc.
print("Saw {0} result(s).".format(len(results)))

# Just loop over it to access the results.
for result in results:
    print("The title is '{0}'.".format(result['title']))


results = solr.search('adfsdf')

# The ``Results`` object stores total results found, by default the top
# ten most relevant results and any additional data like
# facets/highlighting/spelling/etc.
print("Saw {0} result(s).".format(len(results)))

# Just loop over it to access the results.
for result in results:
    print("The title is '{0}'.".format(result['title']))

# For a more advanced query, say involving highlighting, you can pass
# additional options to Solr.
results = solr.search('월넛트리', **{
    'hl': 'true',
    'hl.fragsize': 10,
})

'''# You can also perform More Like This searches, if your Solr is configured
# correctly.
similar = solr.more_like_this(q='id:doc_2', mltfl='text')

# Finally, you can delete either individual documents...
solr.delete(id='doc_1')

# ...or all documents.
solr.delete(q='*:*')'''