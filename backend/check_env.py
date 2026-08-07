import os
vars = ['COGNODB_URI','COGNODB_USERNAME','COGNODB_PASSWORD']
for v in vars:
    present = v in os.environ
    print(f'{v} set: {present}')
