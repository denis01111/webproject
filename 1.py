import os


path = 'C:/'
file = 'e831955s-960.jpg'
for root, dirs, files in os.walk(path):
    if file in files:
        filename = root + '/' + file
        break