from typing import List


def memory_ascii(stack: List[str]):
    top = ' ' + '_' *9 + '\n'
    body = ''
    x = 'ABCDEFGHIJKLMNOP'
    i = 0
    for l in x:
        if i == 3:
            body += '|' + '/' * 9 + '|\n'
            continue
        body += '|' + ' ' * 4 + l + ' ' *4 + '|\n'

        i += 1
    bottom = '|' + '_'*9 + '|'

    print(top+body+bottom)



if __name__ == '__main__':
    memory_ascii()
