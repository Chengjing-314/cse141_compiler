import os
import argparse


class ji_ni_tai_mei_exception(Exception):
    pass

def label_look_up_table(line_number):
    
    look_up_table = {
        1: 0, 
        2: 1,
        29: 3, 
        38: 4,
        43: 5,
        72: 6,
        81: 7,
        15: 8,
        24: 9,
        37: 10,
        44: 11,
        47: 12,
        50: 13,
        62: 14,
        66: 15,
        75: 16,
        78: 17,
        81: 18,
        84: 19,
        27: 20,
        58: 21,
        64: 22,
        79: 23,
        110: 24,
        121: 25,
        124: 26,
        130: 27,
        134: 28,
        3: 29,
        4: 30,
        5: 31,}
    
    look_up_line = look_up_table.get(line_number, None)
    
    if look_up_line == None:
        print(f"ERROR:Invalid line number {line_number} NO LOOK UP TABLE ENTRY FOUND\n")
        return None
    
    return get_immediate(look_up_line, 5)

    
    


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
    #print(reg)
    if reg[0] != 'r':
        return None
    else :
        reg_num = int(reg[1:])
        if reg_num > 2**num_bits - 1:
            print(f"ERROR:Invalid register number {reg_num} (max {2**num_bits - 1})\n")
            return None
        else:
            return bin(reg_num)[2:].zfill(num_bits)
        
def get_immediate(imm, num_bits):
    if isinstance(imm, str) and imm[:2] == '0b':
        imm = int(imm, 2)
    imm = int(imm)
    if imm > 2**num_bits - 1:
        print(f"ERROR:Invalid immediate number {imm} (max {2**num_bits - 1})\n")
        return None
    return bin(imm)[2:].zfill(num_bits)

def assemble_program(source_file, desination_file, label_dict, line_number_dict):
    lines = source_file.readlines()
    total_lines = len(lines)
    line_number = 1
    res = ''
    try:
        for line in lines:
            #print(line_number)
            
            if line_number_dict.get(line_number, None):
                line_number += 1
                continue
            
            cur_line = line.split(' ')
    
            op, optype = get_operator(cur_line[0].lower())
            op1, op2 = None, None
            if optype == 'R':
                op1 = get_resiger(cur_line[1], 3)
                op2 = get_resiger(cur_line[2], 3)
            elif optype == 'I':
                op1 = get_resiger(cur_line[1], 3)
                if cur_line[0].lower() == 'lsl':
                    op2 = '0'+ get_immediate(int(cur_line[2]), 2)
                else:
                    op2 = '1' + get_immediate(int(cur_line[2]), 2)
            elif optype == 'J':
                if cur_line[0].lower() == 'bne':
                    op1 = '0'
                    label_line = get_line_number(cur_line[1], label_dict)
                    op2 = label_look_up_table(label_line)
                else: 
                    op1 = '1'
                    #print(cur_line)
                    op2 = get_immediate(cur_line[1], 5)
                    #print(cur_line[1])
                    # op2 = get_immediate(0, 5)
            else:
                op1 = '000',
                op2 = '000'
            if not(op1 and op2):
                raise ji_ni_tai_mei_exception(f"line{line_number} : Invalid instruction with type {optype} on operands {cur_line[1]} or {cur_line[2]}")
            
            b_lin = op + op1 + op2
            
            if line_number != total_lines :
                res += b_lin + '\n'
            else:
                res += b_lin
            
            line_number += 1
            
        desination_file.write(res)
    
    except ji_ni_tai_mei_exception as e:
        print(str(e))
        os.remove(desination_file)
        return           
    
    except Exception as e:
        os.remove(desination_file)
        raise(e)
    
def sweep_labels(source_file):
    op_keys = ['add', 'mov', 'xor', 'lw', 'sw', 'lsl', \
               'lsr', 'bne', 'set', 'and', 'halt']
    lines = source_file.readlines()
    label_dict = {}
    line_number_dict = {}
    line_number = 1
    for line in lines:
        cur_line = line.split(' ')
        cur_op = cur_line[0].lower()
        if cur_op not in op_keys and cur_op[-2] == ':':
            label_dict[cur_op[:-2]] = line_number
            line_number_dict[line_number] = cur_op
        elif cur_op not in op_keys:
            #print(cur_op[-1])
            raise ji_ni_tai_mei_exception(f"line {line_number} : Invalid OP: {cur_op}")
        line_number += 1
    
    return label_dict, line_number_dict
        
def get_line_number(label, label_dict):
    return label_dict[label.lower().strip(' \n:')]

def main(args):
    source_file = args.f
    desination_file = args.o
    if not os.path.exists(source_file):
        print('Error: Source file does not exist')
        return
    
    sf = open(source_file, 'r')
    df = open(desination_file, 'w+')
    
    # check if destination file have content
    if df.readlines():
        print('ABORT: Destination file is not empty')
        return
    
    label_dict, line_number_dict = sweep_labels(sf)
    #print(label_dict)
    sf.seek(0) # reset file pointer
    assemble_program(sf, df, label_dict, line_number_dict)
    
    df.close()
    sf.close()
        
                
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = 'ISA_compile',description='A simple compiler for 141 ISA')
    parser.add_argument('-f', help='input file, absolute path', required=True)
    parser.add_argument('-o', help='output file name', default='./compiled_isa.txt')
    args = parser.parse_args()
    
    main(args)