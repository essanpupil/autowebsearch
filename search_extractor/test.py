from google_search import GoogleSearch


search = GoogleSearch("unsada")
search.start_search(max_page=2)
#~ for index in range(0, len(search.search_result)):
    #~ print "%d: %s" % (index, search.search_result[index])
#~ 
#~ search.more_search(more_page=2)
#~ for index in range(0, len(search.search_result)):
    #~ print "%d: %s" % (index, search.search_result[index])
