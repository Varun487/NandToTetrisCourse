class SymbolTable(object):
    def __init__(self):
        # Predefined symbols equate to memory locations
        self._symbols \
            = {'SP':0, 'LCL':1, 'ARG':2, 'THIS':3, 'THAT':4,
               'R0':0, 'R1':1, 'R2':2, 'R3':3, 'R4':4, 'R5':5, 'R6':6, 'R7':7,
               'R8':8, 'R9':9, 'R10':10, 'R11':11, 'R12':12, 'R13':13, 'R14':14, 'R15':15,
               'SCREEN':0x4000, 'KBD':0x6000}
                    
    def add_entry(self, symbol, address):
        self._symbols[symbol] = address
        
    def contains(self, symbol):
        return symbol in self._symbols
        
    def get_address(self, symbol):
        return self._symbols[symbol]

def parse(name):
    #removes comments, removes whitespaces, remove \n,returns only broken instructions
    filehandle_read = open(name+'.asm',"r")
    filereadlines = filehandle_read.readlines()
    nextaddress = 16
    l = []
    
    for line in filereadlines:
        line = line.strip()
        if ((line!='') or (line!='\n')or (line[0] == '@') or (line[0] == 'D') or (line[0] == 'A') or line[0] == 'M') or (line[0] == '0') or (line[0]=='('):
            s=""
            i=0
            while((i<len(line)) and (line[i]!='\n') and (line[i]!=' ') and (line[i]!='/')):
                s+=line[i]
                i+=1
            l.append(s)
    l = list(filter(lambda x:x!='',l))
    filehandle_read.close()
    print(l)
    for line in l:
        if line[0] == '(':
            s=''
            i=1
            while(line[i]!=')'):
                s+=line[i]
                i+=1
            print(s)
            SymbolTable.add_entry(s,nextaddress)
            nextaddress+=1
    return l

def c_instruct_translator(dest,comp,jump):
    instruct = '111'
    dest_table = {'':'000', 'M':'001', 'D':'010', 'MD':'011', 'A':'100', 'AM':'101', 'AD':'110', 'AMD':'111'}
    jump_table = {'':'000', 'JGT':'001', 'JEQ':'010', 'JGE':'011', 'JLT':'100', 'JNE':'101', 'JLE':'110', 'JMP':'111'}
    comp_table = {'0': '0101010',
        '1': '0111111',
        '-1': '0111010',
        'D': '0001100',
        'A': '0110000',
        '!D': '0001101',
        '!A': '0110001',
        '-D': '0001111',
        '-A': '0110011',
        'D+1': '0011111',
        'A+1': '0110111',
        'D-1': '0001110',
        'A-1': '0110010',
        'D+A': '0000010',
        'D-A': '0010011',
        'A-D': '0000111',
        'D&A': '0000000',
        'D|A': '0010101',
        'M': '1110000',
        '!M': '1110001',
        '-M': '1110011',
        'M+1': '1110111',
        'M-1': '1110010',
        'D+M': '1000010',
        'D-M': '1010011',
        'M-D': '1000111',
        'D&M': '1000000',
        'D|M': '1010101'}
    instruct += comp_table[comp]
    instruct += dest_table[dest]
    instruct += jump_table[jump]
    return instruct


def translator(name):
    l = parse(name)
    for line in range(len(l)):
        num=""
        if l[line][0] == '@':
            if l[line][1].isnum():
                for i in range(1,len(l[line])):
                    num+=l[line][i]
                num = str(bin(int(num)).replace("0b",""))
                num = ('0'*(15 - len(num))) + num
                l[line] = '0' + num
            else:
                # to handle is a symbol is present
                pass
        
        else:
            dest=""
            comp=""
            jump=""
            equalpassed = False
            semicolonpassed = False
            i=0
            while(i<len(l[line])):
                if l[line][i]=='=':
                    equalpassed = True
                    i+=1
                if l[line][i]==';':
                    semicolonpassed = True
                    i+=1
                if (not(equalpassed) and not(semicolonpassed) and ('=' in l[line])):
                        dest+=l[line][i]
                if ((equalpassed) and not(semicolonpassed)) or (('=' not in l[line]) and not(semicolonpassed)):
                    comp+=l[line][i]
                if (semicolonpassed):
                    jump+=l[line][i]
                i+=1
            l[line] = c_instruct_translator(dest,comp,jump)
    return l

def assembler(name):
    file_handle_write = open(name+'.hack','w+')
    l = translator(name)
    for i in l:
        file_handle_write.write(i+'\n')

parse("Max")