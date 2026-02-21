from math import floor

def daily_calorie_consumption(weight, height, age, gender="male", activity_level=1.2):

    bmr = 0

    if gender == "male":

        bmr = weight*10 + height*6.25 - 5*age + 5

    else :

        bmr = weight*10 + height*6.25 - 5*age - 161


    calorie = bmr * activity_level

    return floor(calorie)



print(daily_calorie_consumption(55, 165, 32))
