module PC_LUT_2(
  input       [ 1:0] index,	   // target 4 values
  output logic[7:0] value);

  always_comb case(index)
    0: value = 3;
	1: value = 2;
	2: value = 'b1; 
	default: value = 'b0; 
  endcase

endmodule