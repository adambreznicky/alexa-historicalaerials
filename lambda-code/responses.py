class alexa:
    '''
    Class of predefined Alexa responses
    '''
    def __init__(self):
        self.reprompt_1 = "Is there another county you would " \
                          "like me to look up? "
        self.reprompt_2 = "If there is another county I can lookup " \
                          "I would be happy to do so. "
        self.reprompt_3 = "Is there another year you would " \
                          "like me to look up? "
        self.instruction = "Please tell me the Texas county you would " \
                           "like historic imagery for and I can tell you " \
                           "what we have in our archive. "
        self.confused = "I'm not sure what county you're looking for. "
        self.confused_2 = "I'm not sure what year you're looking for. "

    def imagery_range(self, county, total, min_year, max_year):
        text = "TinRiss has " + str(total) + " years of " \
               + county + " County historical " \
               "imagery available ranging from " + \
               str(min_year) + " to " + str(max_year) + ". "
        return text

    def imagery_none(self, county):
        text = "Sorry, there is no historical imagery " + \
               "for " + county + " County. "
        return text

    def imagery_single(self, county, single_year):
        text = "TinRiss has 1 year of " + county + \
               " County historical imagery available. " \
               "It is from " + str(single_year) + ". "
        return text

    def list_range(self, county, years):
        year_list_str = ""
        for y in years[:-1]:
            year_str = str(y) + ", "
            year_list_str += year_str
        year_last = "and " + str(years[-1])
        year_list_str += year_last
        text = "TinRiss has " + county + " County historical " \
               "imagery available for years " + \
               year_list_str + ". "
        return text

    def affirmative_year(self, county, year):
        text = "Yes, " + str(year) + " is available for " + \
               county + " County. "
        return text

    def negative_year(self, county, year, close_year):
        text = "Sorry, " + str(year) + " is not available for " + \
               county + " County. The closest year on file to " + \
               str(year) + " is " + str(close_year) + ". "
        return text

    def negative_year_single(self, county, year, single_year):
        text = "Sorry, " + str(year) + " is not available. " + \
               "The only year on file for " + county + " County " \
               " is " + str(single_year) + ". "
        return text
