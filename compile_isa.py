import os
import argparse


class ji_ni_tai_mei_exception(Exception):
    pass


def get_operator(op):
    operators = {
        'add': '000',
        'mov': '001',
        'xor': '010',
        'lw': '011',
        'sw': '100',
        'lsl': '101',
        'lsr': '101',
        'bne': '110',
        'set': '110',
        'and': '111',
        'halt': '000'
    }
    
    operator_types = {
        'add': 'R',
        'mov': 'R',
        'xor': 'R',
        'lw': 'R',
        'sw': 'R',
        'and': 'R',
        'lsl': 'I',
        'lsr': 'I',
        'bne': 'J',
        'set': 'J',
        'halt': 'H'
    }
    
    return operators[op], operator_types[op]
    
def get_resiger(reg, num_bits):
    if reg[0] != 'r':
        return None
    else :
        reg_num = int(reg[1:])
        if reg_num > 2**num_bits - 1:
            return None
        else:
            return bin(reg_num)[2:].zfill(num_bits)
        
def get_immediate(imm, num_bits):
    if isinstance(imm, str) and imm[:2] == '0b':
        imm = int(imm)
    if imm > 2**num_bits - 1:
        return None
    return bin(imm)[2:].zfill(num_bits)

def main(args):
    source_file = args.f
    desination_file = args.o
    if not os.path.exists(source_file):
        print('Error: Source file does not exist')
        return
    

    sf = open(source_file, 'r')
    lines = sf.readlines()
    
    df = open(desination_file, 'w')
    
    line_number = 1
    try:
        for line in lines:
            cur_line = line.split(' ')
            res = ''
            op, optype = get_operator(cur_line[0].lower())
            op1, op2 = None, None
            if optype == 'R':
                op1 = get_resiger(cur_line[1], 3)
                op2 = get_resiger(cur_line[2], 3)
            elif optype == 'I':
                op1 = get_resiger(cur_line[1], 3)
                op2 = get_immediate(int(cur_line[2]), 3)
            elif optype == 'J':
                if cur_line[0].lower() == 'bne':
                    op1 = '0'
                    op2 = get_immediate(int(cur_line[1]), 5)
                else: # FIXME: SET NEED TO BE FIXED
                    op1 = '000'
                    op2 = '000'
            else:
                op1 = '000',
                op2 = '000'
            if not(op1 and op2):
                raise ji_ni_tai_mei_exception(f"line{line_number} : Invalid instruction with type {optype} on operands {cur_line[1]} and {cur_line[2]}")
            
            res = op + op1 + op2
            if line == lines[-1]:
                df.write(res)
            else:
                df.write(res + '\n')
            
            line_number += 1
        
        df.close()
        sf.close()
        
                
    except ji_ni_tai_mei_exception as e:
        print(str(e))
        os.remove(desination_file)
        return           
    
    except Exception as e:
        os.remove(desination_file)
        raise(e)
    





if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = 'ISA_compile',description='A simple compiler for 141 ISA')
    parser.add_argument('-f', help='input file, absolute path')
    parser.add_argument('-o', help='output file name', default='./compiled_isa.txt')
    args = parser.parse_args()
    
    main(args)
    

