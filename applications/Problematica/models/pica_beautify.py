#Supplies methods for cleaning up expressions such as dates and numbers

import math


class PicaBeautify:

    @staticmethod
    def clean_date(date):
        return "{:%m/%d/%Y}".format(date)

    @staticmethod
    def clean_number(number): #rounds large numbers into K,M,B
        unitSymbol = ['','K','M','B','T']
        if number < 1000 and type(number) == int:
            return str(number)
        else:
            base = 1000
            exponent = int(math.floor(math.log(number,base)))
            coefficient = number/(math.pow(base,exponent))
            #We want 3 digits in final number
            roundTo = 3 - len(str(int(coefficient)))
            if roundTo != 0: result = str(round(coefficient, roundTo))+unitSymbol[exponent]
            else: result = str(int(coefficient))+unitSymbol[exponent]

        return result

    #Made using http://stackoverflow.com/questions/1551382/user-friendly-time-format-in-python
    @staticmethod
    def time_elapsed_since(time=False):
        """turns a date into the form '30s ago'  """
        from datetime import datetime
        now = datetime.now()
        if type(time) is int:
            diff = now - datetime.fromtimestamp(time)
        elif isinstance(time,datetime):
            diff = now - time
        elif not time:
            diff = now - now
        second_diff = diff.seconds
        day_diff = diff.days

        if day_diff < 0:
            return ''

        if day_diff == 0:
            if second_diff < 10:
                return "just now"
            if second_diff < 60:
                return str(second_diff) + "s ago"
            if second_diff < 120:
                return "a minute ago"
            if second_diff < 3600:
                return str(second_diff / 60) + "m ago"
            if second_diff < 7200:
                return "an hour ago"
            if second_diff < 86400:
                return str(second_diff / 3600) + "h ago"
        if day_diff == 1:
            return "Yesterday"
        if day_diff < 7:
            return str(day_diff) + "d ago"
        if day_diff < 31:
            return str(day_diff / 7) + "w ago"
        if day_diff < 365:
            return str(day_diff / 30) + "m ago"
        return str(day_diff / 365) + "yr ago"
