import os
import argparse
#                       _oo0oo_
#                      o8888888o
#                      88" . "88
#                      (| -_- |)
#                      0\  =  /0
#                    ___/`---'\___
#                  .' \\|     |# '.
#                 / \\|||  :  |||# \
#                / _||||| -:- |||||- \
#               |   | \\\  -  #/ |   |
#               | \_|  ''\---/''  |_/ |
#               \  .-\__  '-'  ___/-. /
#             ___'. .'  /--.--\  `. .'___
#          ."" '<  `.___\_<|>_/___.' >' "".
#         | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#         \  \ `_.   \_ __\ /__ _/   .-` /  /
#     =====`-.____`.___ \_____/___.-`___.-'=====
#                       `=---='
#
#
#     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#               佛祖保佑         永无BUG

class ji_ni_tai_mei_exception(Exception):
    pass

def label_look_up_table(line_number):
    
    # program 1 look_up_table 
        # 7: 0, 
        # 47: 1,
        # 56: 2,
        # 58: 3, 
        # 66: 4,
        # 75: 5,
        # 77: 6,
        # 107: 7,
        # 114: 8,
        # 121: 9,
        # 128: 10,
        # 148: 11,
    # program 2 look_up_table
        # 7: 0, 
        # 206: 1,
        # 22: 12,
        # 29: 13,
        # 36: 14,
        # 43: 15,
        # 62: 16,
        # 71: 17,
        # 73: 18,
        # 80: 19,
        # 89: 20,
        # 91: 21,
        # 115: 22,
        # 118: 23,
        # 120: 24,
        # 131: 25,
        # 144: 26,
        # 146: 27,
        # 156: 28,
        # 159: 29,
        # 168: 30,
        # 170: 31,
    look_up_table = {
        7: 0, 
        206: 1,
        56: 2,
        58: 3, 
        66: 4,
        75: 5,
        77: 6,
        107: 7,
        114: 8,
        121: 9,
        128: 10,
        148: 11,
        22: 12,
        29: 13,
        36: 14,
        43: 15,
        62: 16,
        71: 17,
        73: 18,
        80: 19,
        89: 20,
        91: 21,
        115: 22,
        118: 23,
        120: 24,
        131: 25,
        144: 26,
        146: 27,
        156: 28,
        159: 29,
        168: 30,
        170: 31,}
    
    # FIXME: This is a hack to get the program to compile
    
    look_up_line = look_up_table.get(line_number, None)
    
    # if look_up_line == None:
    #     print(f"ERROR:Invalid line number {line_number} NO LOOK UP TABLE ENTRY FOUND\n")
    #     return None
    
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
    
def get_register(reg, num_bits):
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

def assemble_program(source_file, destination_file, label_dict):
    lines = source_file.readlines()
    total_lines = len(lines)
    line_number = 1
    res = ''
    try:
        for line in lines:
            #print(line_number)
            
            if label_dict.get((line.split(' '))[0][:-2].lower(), None):
                line_number += 1
                continue
            
            cur_line = line.split(' ')
    
            op, optype = get_operator(cur_line[0].lower())
            op1, op2 = None, None
            if optype == 'R':
                op1 = get_register(cur_line[1], 3)
                op2 = get_register(cur_line[2], 3)
            elif optype == 'I':
                op1 = get_register(cur_line[1], 3)
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
            
        destination_file.write(res)
    
    except ji_ni_tai_mei_exception as e:
        print(str(e))
        os.remove(destination_file)
        return           
    
    except Exception as e:
        os.remove(destination_file)
        raise(e)
    
def sweep_labels(source_file):
    op_keys = ['add', 'mov', 'xor', 'lw', 'sw', 'lsl', \
               'lsr', 'bne', 'set', 'and', 'halt']
    lines = source_file.readlines()
    label_dict = {}
    line_number_dict = {}
    line_number = 1
    branch_offset = 0
    for line in lines:
        cur_line = line.split(' ')
        cur_op = cur_line[0].lower()
        if cur_op not in op_keys and cur_op[-2] == ':':
            label_dict[cur_op[:-2]] = line_number - branch_offset
            line_number_dict[line_number - branch_offset] = cur_op
            branch_offset += 1
        elif cur_op not in op_keys:
            #print(cur_op[-1])
            raise ji_ni_tai_mei_exception(f"line {line_number} : Invalid OP: {cur_op}")
        line_number += 1
    
    return label_dict
        
def get_line_number(label, label_dict):
    return label_dict[label.lower().strip(' \n:')]

def main(args):
    source_file = args.f
    destination_file = args.o
    if not os.path.exists(source_file):
        print('Error: Source file does not exist')
        return
    
    sf = open(source_file, 'r')
    df = open(destination_file, 'w+')
    
    # check if destination file have content
    if df.readlines():
        print('ABORT: Destination file is not empty')
        return
    
    label_dict = sweep_labels(sf)
    print(label_dict)
    sf.seek(0) # reset file pointer
    assemble_program(sf, df, label_dict)
    
    df.close()
    sf.close()
        
                
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = 'ISA_compile',description='A simple compiler for 141 ISA')
    parser.add_argument('-f', help='input file, absolute path', required=True)
    parser.add_argument('-o', help='output file name', default='./compiled_isa.txt')
    args = parser.parse_args()
    
    main(args)