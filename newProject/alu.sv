// combinational -- no clock
// sample -- change as desired
module alu(
  input[3:0] alu_cmd,    // ALU instructions
  input[7:0] inA, inB,	 // 8-bit wide data path
  input      sc_i,       // shift_carry in
  input[2:0] shift_value,
  output logic[7:0] rslt,
  output logic sc_o,     // shift_carry out
               pari,     // reduction XOR (output)
			   zero      // NOR (output)
);
	logic [2:0] alu_cmd_YiPie;
always_comb begin 
  alu_cmd_YiPie = alu_cmd[3:1];
  rslt = 'b0;            
  sc_o = 'b0;    
  zero = !rslt;
  pari = ^rslt;
  if (alu_cmd_YiPie == 3'b110) begin
    case(alu_cmd)
      4'b1100: begin //bne
        rslt = |inA;
		    zero = |inA;
		  end
      4'b1101: //set
        rslt = inB;
    endcase
  end
  else begin
    case(alu_cmd_YiPie)
      3'b000: // add 2 8-bit unsigned; automatically makes carry-out
        rslt = inA + inB;
      3'b001: // mov
        rslt = inB;
      3'b010: // xor
        rslt = inA ^ inB;
      3'b101: begin // logical shift
		case(shift_value)
			3'b001:
				{sc_o,rslt} = {inA,1'b0};
			3'b010:
				{sc_o,rslt} = {inA[6:0],2'b0};
			3'b011:
				{sc_o,rslt} = {inA[5:0],3'b0};
			3'b101:
				{rslt,sc_o} = {1'b0,inA};
			3'b110:
				{rslt,sc_o} = {1'b0,inA[7:1]};
			3'b111:
				{rslt,sc_o} = {1'b0,inA[7:2]};
			default:
				rslt = inA;
		endcase
      end
      3'b111: // and
        rslt = inA & inB;
    endcase
  end
  
end
   
endmodule