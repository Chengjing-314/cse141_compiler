

def hamming_encoding(data1, data2):
    # data1 upper 8 bits, data2 lower 8 bits
    temp_data1 = data1
    temp_data2 = data2 
    
    # format data1 and data2 to 16 bits
    temp_data1 = temp_data1  << 5 # 00000111 -> 11100000 
    upper4 = temp_data2 & 0b11110000 
    upper4 = upper4 >> 3   #11110000 -> 00011110
    temp_data1 = temp_data1 + upper4
    
    data_2_4_2 = temp_data2 & 0b1110
    data_2_4_2 = data_2_4_2 << 4 
    data_2_1 = temp_data2 & 0b1
    data_2_1 = data_2_1 << 3
    temp_data2 = data_2_4_2 + data_2_1
    
    data_1 = temp_data1
    data_2 = temp_data2
    
    cnt = 8
    res = 0
    while (cnt <= 15):
        cbit = temp_data1 & 1
        temp_data1 = temp_data1 >> 1
        if (cbit == 1):
            res = res ^ cnt 
        cnt = cnt + 1
    
    temp_data2 = temp_data2 >> 1
    cnt = 1
    while (cnt <= 7):
        cbit = temp_data2 & 1
        temp_data2 = temp_data2 >> 1
        if (cbit == 1):
            res = res ^ cnt 
        cnt = cnt + 1
    
    # data1 and data2 are formatted to 16 bits

    
    
    p1_p2 = (res & 0b11) << 1
    p4 = (res & 0b100) << 2
    p8 = (res & 0b1000) >> 3
    
    data_2 = data_2 + p1_p2 + p4
    data_1 = data_1 + p8
    
    print("res: ", format(res, 'b'))
    
    # calculate parity bit p0
    parity_0 = 0 
    cnt = 0
    temp_data1 = data_1
    temp_data2 = data_2
    while (cnt < 8):
        parity_0 = parity_0 ^ (temp_data1 & 1)
        temp_data1 = temp_data1 >> 1
        cnt = cnt + 1
    
    cnt = 0 
    
    while (cnt < 8):
        parity_0 = parity_0 ^ (temp_data2 & 1)
        temp_data2 = temp_data2 >> 1
        cnt = cnt + 1
    
    data_2 = data_2 + parity_0
    
    str_data_2 = format(data_2, 'b')
    if len(str_data_2) < 8:
        str_data_2 = '0' * (8 - len(str_data_2)) + str_data_2
    str_data_1 = format(data_1, 'b')
    if len(str_data_1) < 8:
        str_data_1 = '0' * (8 - len(str_data_1)) + str_data_1
   
    print(str_data_1 + str_data_2)


hamming_encoding(0b00000000, 0b00000001)
    
        