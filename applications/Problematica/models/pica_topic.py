#pica is short for problematica
#Here and ONLY here topic database calls are handled

class PicaTopic:
    #Constructor ===========================================================
    def __init__(self, topic_id):
        if topic_id == "fromEntry": #for constructing using a database entry
            self.db_problem = None
        else:
            try:
                query = db.topics.id == topic_id
                topic = db(query).select().first()
                self.db_topic = topic
            except:
                self.db_topic = None

    #constructs from database Row object. Use when possible to save time.
    @staticmethod
    def fromEntry(entry):
        newTopic = PicaTopic("fromEntry")
        newTopic.db_topic = entry
        return newTopic

    #Static Methods ========================================================
    @staticmethod
    def get_all_topics():
        db_topic_list = db().select(db.topics.ALL, orderby="topics.topic_name ASC")
        topic_list = []
        for i in db_topic_list:
            topic_list.append(PicaTopic.fromEntry(i))
        return topic_list

    @staticmethod
    def get_id_by_topic_name(name):
        query = db.topics.topic_name == name
        db_result = db(query).select().first()
        if db_result is None:
            return -1
        else:
            return db_result.id

    @staticmethod
    def get_everything_topic(): #returns the topic 'ALL'
        everything_topic_id = PicaTopic.get_id_by_topic_name('All')
        everything_topic = PicaTopic(everything_topic_id)
        return everything_topic

    @staticmethod
    def search(searchInput): #returns topics relating to search input
        searchInput = searchInput.split(' ')
        query = db.topics.topic_name.contains(searchInput, all=False)
        db_results = db(query).select()
        results = []
        for i in db_results:
            results.append(PicaTopic(i.id))
        return results

    #Getter Methods ========================================================
    def get_id(self):
        return self.db_topic.id

    def get_name(self):
        return self.db_topic.topic_name

    def get_description(self):
        return self.db_topic.topic_description

    def get_URL(self):
        return URL('topic',args=(self.get_name()))

    def is_found_in_database(self):
        if self.db_topic is None:
            return False
        else:
            return True



    #Setter Methods ========================================================
