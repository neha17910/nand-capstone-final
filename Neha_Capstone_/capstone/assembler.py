from pathlib import Path
import sys
import re

COMP = dict(zip('0 1 -1 D A !D !A -D -A D+1 A+1 D-1 A-1 D+A D-A A-D D&A D|A'.split(), '0101010 0111111 0111010 0001100 0110000 0001101 0110001 0001111 0110011 0011111 0110111 0001110 0110010 0000010 0010011 0000111 0000000 0010101'.split()))
COMP.update({k.replace('A','M'): '1'+v[1:] for k,v in list(COMP.items()) if 'A' in k})
JUMP = {k:format(i,'03b') for i,k in enumerate(['','JGT','JEQ','JGE','JLT','JNE','JLE','JMP'])}

def assemble(path):
    path = Path(path)
    symbols = {f'R{i}':i for i in range(16)}
    symbols.update(SP=0,LCL=1,ARG=2,THIS=3,THAT=4,SCREEN=16384,KBD=24576)
    lines = []
    # Pass 1: record labels and ROM addresses.
    for n, raw in enumerate(path.read_text().splitlines(),1):
        line = ''.join(raw.split('//')[0].split())
        if not line: continue
        if line.startswith('(') and line.endswith(')'):
            symbols[line[1:-1]] = len(lines)
        else: lines.append((n,line))
    # Pass 2: allocate variables and encode instructions.
    result = []
    next_ram = 16
    for n,line in lines:
        try:
            if line.startswith('@'):
                name = line[1:]
                if name.isdigit(): value = int(name)
                else:
                    if not re.fullmatch(r'[A-Za-z_.$:][\w.$:]*',name): raise ValueError('invalid symbol')
                    if name not in symbols:
                        symbols[name] = next_ram
                        next_ram += 1
                    value = symbols[name]
                if not 0 <= value < 32768: raise ValueError('address out of range')
                result.append(format(value,'016b'))
            else:
                dest, sep, rest = line.partition('=')
                if not sep: dest,rest = '',dest
                comp, sep, jump = rest.partition(';')
                if any(c not in 'ADM' for c in dest) or len(set(dest)) != len(dest): raise ValueError('invalid destination')
                result.append('111'+COMP[comp]+''.join('1' if c in dest else '0' for c in 'ADM')+JUMP[jump])
        except (KeyError, ValueError) as e:
            raise ValueError(f'Line {n}: invalid instruction ({e})') from e
    path.with_suffix('.hack').write_text('\n'.join(result)+'\n')
    path.with_name('symbols.txt').write_text(''.join(f'{k} = {v}\n' for k,v in symbols.items()))
    print('Created',path.with_suffix('.hack'))

if __name__ == '__main__':
    assemble(sys.argv[1] if len(sys.argv)>1 else 'Box.asm')
