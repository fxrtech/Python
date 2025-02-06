import time
import sys

counter = 1

print('Happy Mothers Day!!')
while counter < 15:
    gift = sys.stdout.write('{0}{1}{2}\r'.format(chr(56), chr(61) * counter, chr(68)))
    sys.stdout.flush()
    time.sleep(0.1)
    if counter == 14:
        sys.stdout.write('{0}{1}{2} {3}\n'.format(chr(56), chr(61) * counter, chr(68), chr(126) * 7))
    counter += 1
