module PC_LUT #(parameter D=12)(
  input       [ 4:0] addr_lut,	   // target 4 values
  output logic[D-1:0] target);

  always_comb case(addr_lut)
    0: target = 7;
	1: target = 206; 
	2: target = 56;  
	3: target = 58;
	4: target = 66;
	5: target = 75;
	6: target = 77;
	7: target = 107;
	8: target = 114;
	9: target = 121;
	10: target = 128;
	11: target = 148;
	12: target = 22;
	13: target = 29;
	14: target = 36;
	15: target = 43;
	16: target = 62;
	17: target = 71;
	18: target = 73;
	19: target = 80;
	20: target = 89;
	21: target = 91;
	22: target = 115;
	23: target = 118;
	24: target = 120;
	25: target = 131;
	26: target = 144;
	27: target = 146;
	28: target = 156;
	29: target = 159;
	30: target = 168;
	31: target = 170;
	default: target = 'b0;  // hold PC  
  endcase

endmodule

/*

	   pc = 4    0000_0000_0100	  4
	             1111_1111_1111	 -1

                 0000_0000_0011   3

				 (a+b)%(2**12)


   	  1111_1111_1011      -5
      0000_0001_0100     +20
	  1111_1111_1111      -1
	  0000_0000_0000     + 0


  */
