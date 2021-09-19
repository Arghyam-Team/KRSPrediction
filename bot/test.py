import datefinder

a = "next 12/05/2021 trend"
match = datefinder.find_dates(a)
for i in match:
    print(i)