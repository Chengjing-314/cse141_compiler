module PC_LUT #(parameter D=12)(
  input       [ 4:0] addr_lut,	   // target 4 values
  output logic[D-1:0] target);
  
  always_comb case(addr_lut)
    0: target = 7;
	1: target = 47; 
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
	12: target = 47;
	13: target = 50;
	14: target = 62;
	15: target = 66;
	16: target = 75;
	17: target = 78;
	18: target = 81;
	19: target = 84;
	20: target = 27;
	21: target = 58;
	22: target = 64;
	23: target = 79;
	24: target = 110;
	25: target = 121;
	26: target = 124;
	27: target = 130;
	28: target = 134;
	29: target = 1;
	30: target = 1;
	31: target = 1;
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
