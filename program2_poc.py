def hamming_decode(data1, data2):
    tmp_data1 = data1
    tmp_data2 = data2
    
    p0_check = 0
    cnt = 0 
    while (cnt < 8):
        p0_check = p0_check ^ (tmp_data1 & 1)
        tmp_data1 = tmp_data1 >> 1
        cnt = cnt + 1
        
    cnt = 0 
    while (cnt < 8): 
        p0_check = p0_check ^ (tmp_data2 & 1)
        tmp_data2 = tmp_data2 >> 1
        cnt = cnt + 1
    
    tmp_data1 = data1
    tmp_data2 = data2 >> 1
    
    cnt = 1
    res = 0
    while (cnt <= 7):
        cbit = tmp_data2 & 1
        tmp_data2 = tmp_data2 >> 1
        if (cbit == 1):
            res = res ^ cnt 
        cnt = cnt + 1
    
    cnt = 8
    while (cnt <= 15):
        cbit = tmp_data1 & 1
        tmp_data1 = tmp_data1 >> 1
        if (cbit == 1):
            res = res ^ cnt 
        cnt = cnt + 1
        
    print("res: ", format(res, 'b'))
        
    indicator = 0
    
    if (p0_check == 0 and res == 0):
        print("No error")
        indicator = 0b00000000
        
        
    elif (p0_check == 0 and res != 0):
        print("Two errors")
        indicator = 0b11000000
        
    elif (p0_check != 0 and res == 0):
        print("One error at parity bit 0")
        data2 = data2 ^ 1
        indicator = 0b01000000
    
    else:
        print("One error at bit: ", res)
        if (res > 8):
            data1 = data1 ^ (1 << (res - 8))
        else:
            data2 = data2 ^ (1 << res)
        
        indicator = 0b01000000
        
    data_2_4_2 = (data2 & 0b11100000) >> 4 # 11100000 -> 00001110
    data_2_1 = (data2 & 0b1000) >> 3
    
    data_1_8_5 = (data1 & 0b00011110) << 3 # 00011110 -> 11110000
    data1 = data1 >> 5 
    data2 = data_2_4_2 + data_2_1 + data_1_8_5
    
    data1 += indicator    
    
        
    str_data_2 = format(data2, 'b')
    if len(str_data_2) < 8:
        str_data_2 = '0' * (8 - len(str_data_2)) + str_data_2
    str_data_1 = format(data1, 'b')
    if len(str_data_1) < 8:
        str_data_1 = '0' * (8 - len(str_data_1)) + str_data_1
   
    print(str_data_1 + str_data_2)


hamming_decode(0b00000000 , 0b00001111)
        
        
    
    
    
    