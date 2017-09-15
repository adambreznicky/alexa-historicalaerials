class alexa:
    '''
    Class of predefined Alexa responses
    '''
    def __init__(self):
        self.reprompt_1 = "Is there another county you would " \
                          "like me to look up? "
        self.reprompt_2 = "If there is another county I can lookup " \
                          "I would be happy to do so. "
        self.instruction = "Please tell me the Texas county you would " \
                           "like historic imagery for and I can tell you " \
                           "what we have in our archive. "
        self.confused = "I'm not sure what county you're looking for. "

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
