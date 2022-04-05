import os
times = input('How many times should the program run:')
for i in range(int(times)):
    print(i)
    os.system("python Hangman.py 1 _ _ _ 0")  
input('Finished...')
