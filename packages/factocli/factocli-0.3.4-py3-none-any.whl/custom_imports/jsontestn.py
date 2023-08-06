import json




with open("settings.json", 'r') as f:
    contents = json.load(f)
    print(contents)
    contents['factorio-path'] = "benaanski"
    contents['benaan'] = True
    
print(contents)


with open("settings.json", 'w') as a:
    #a.write(contents)
    json.dumps(contents)
    
# data = json.load('settings.json')
# data['factorio-path'] = 'Benaaskiiiiii'
# json.dump('settings.json', data)



