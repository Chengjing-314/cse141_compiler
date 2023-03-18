module PC_LUT_2(
  input       [ 4:0] index,	   // target 4 values
  output logic[7:0] value);

  always_comb case(index)
    0: value = 0;
    1: value = 1;
    2: value = 2;
    3: value = 3;
    4: value = 4;
    8: value = 8;
    14: value = 14;
    15: value = 15;
    16: value = 16;
    17: value = 17;
    18: value = 18;
    24: value = 24;
    30: value = 30;
    31: value = 31;
    25: value = 65024;
    26: value = 112;
    27: value = 33;
    28: value = 34;
    29: value = 35;
    5: value = 72;
    6: value = 70;
    7: value = 71;
    9: value = 9;
    10: value = 10;
	  11: value = 11;
    12: value = 12;
    13: value = 13;
    19: value = 19;
    20: value = 20;
    21: value = 21;
    22: value = 22;
    23: value = 23;
    
    default: value = 'b0; 
  endcase

endmodule