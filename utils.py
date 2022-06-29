from typing import List


def memory_ascii(stack: List[str], arrow_idx: int = -1):
    top = '   +' + '-' *9 + '+\n'
    body = ''
    for i, space in enumerate(stack):
        new_str = str(i+1) + ' ' * (3 - len(str(i+1)))
        if space == 'X':
            new_str += '|' + '/' * 9 + '|'
        elif space == 'FREE':
            new_str += '|' + ' ' * 9 + '|'
        else:
            new_str += '|' + ' ' * 4 + space + ' ' *4 + '|'
        
        if arrow_idx > -1:
            new_str += ' <---'
        body += new_str + '\n'

    bottom = '   +'+ '-'*9 + '+'

    print(top+body+bottom)