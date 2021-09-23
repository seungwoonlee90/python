class Car() :
    """
    Car Class
    Author : Ethan Lee
    Date : 2021. 09. 23.
    Describe : Today I learned Class and Methods
    """

    def __init__(self, company, details):
       self._company = company
       self._details = details

    def __str__(self):
        return 'str : {} - {} '.format(self._company, self._details)

car1 = Car('Ferrari', {'color' : 'Red', 'horsepower' : 400, 'price':8000})
print(car1)