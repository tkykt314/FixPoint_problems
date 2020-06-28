import csv
dicto = {str(k) : 1 for k in range(26)}
print(dicto)
l = {}
try:
    with open("dict.csv",'r') as f:
        print("ok")
        reader = csv.DictReader(f)
        l = [row for row in reader][0]
        print(l)
        for i in range(len(dicto.keys())):
            key = list(dicto.keys())[i]
            try:
                l[key] = str(int(l[key]) + dicto[key])
            except:
                l[key] = dicto[key]
        print(l)

        with open("dict.csv",'w') as f:
            print("last")
            writer = csv.DictWriter(f, dicto.keys())
            writer.writeheader()
            writer.writerow(l)

except FileNotFoundError:
    print("fuck")
    with open("dict.csv",'w') as f:
        writer = csv.DictWriter(f, dicto.keys())
        writer.writeheader()
        writer.writerow(dicto)

for i in range(1, 10):
    print(i)


