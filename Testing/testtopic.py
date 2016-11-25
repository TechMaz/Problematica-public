print "========================================"

class TestTopicMethods:
    #topic get_name() doesn't work
    @staticmethod
    def test_get_all_topics():
        try:
            topics = PicaTopic.get_all_topics()
            """
            for topic in topics:
                print topic.getname()
            """
            print topics
            print "test get_firstname successful\n"
        except:
            print "test get_firstname unsuccessful\n"
