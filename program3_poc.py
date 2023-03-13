def pattern_search(txt):
    # text = 8 bit wide 2d, pattern = 5 bit
    outer = 0 
    byte_cnt = 0 
    occ_cnt = 0
    
    pattern = (txt[32] & 0b11111000) >> 3

    while (outer < 32):
        cur = txt[outer]
        inner = 0 
        occ_flag = 0 
        while (inner < 4):
            lower_5 = cur & 0x00011111
            cur = cur >> 1
            if (lower_5 == pattern):
                occ_flag = 1
                byte_cnt += 1
            inner += 1
        occ_cnt += occ_flag
        outer += 1
    
    txt[33] = byte_cnt
    txt[34] = occ_cnt
    
    outer = 0 
    while (outer < 31):
        upper = (txt[outer] & 0b00001111) << 4
        lower = (txt[outer+1] & 0b11110000) >> 4
        cur = upper + lower
        inner = 0
        while (inner < 4):
            lower_5 = cur & 0x00011111
            cur = cur >> 1
            if (lower_5 == pattern):
                byte_cnt += 1
            inner += 1
        outer += 1
    
    txt[35] = byte_cnt
    
    print(txt[33], txt[34], txt[35])

test_data = [0] * 36
test_data[32] = 8 # 00001000
test_data[0] = 1 # 00000001

pattern_search(test_data)