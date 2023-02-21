// combinational -- no clock
// sample -- change as desired
module alu(
  input[3:0] alu_cmd,    // ALU instructions
  input[7:0] inA, inB,	 // 8-bit wide data path
  input      sc_i,       // shift_carry in
  output logic[7:0] rslt,
  output logic sc_o,     // shift_carry out
               pari,     // reduction XOR (output)
			   zero      // NOR (output)
);

always_comb begin 
  logic [2:0] alu_cmd_YiPie = alu_cmd[3:1];
  rslt = 'b0;            
  sc_o = 'b0;    
  zero = !rslt;
  pari = ^rslt;
  if (alu_cmd_YiPie == 3'b110) begin
    case(alu_cmd)
      4'b1100: //bne
        zero = !(|inA);
      4'b1101: //set
        rslt = inB;
    endcase
  end
  else begin
    case(alu_cmd_YiPie)
      3'b000: // add 2 8-bit unsigned; automatically makes carry-out
        {sc_o,rslt} = inA + inB + sc_i;
      3'b001: // mov
        rslt = inB;
      // {sc_o,rslt} = {inA, sc_i};
      //   /*begin
      // rslt[7:1] = ina[6:0];
      // rslt[0]   = sc_i;
      // sc_o      = ina[7];
      //   end*/
      3'b010: // xor
        rslt = inA ^ inB;
      3'b101: begin // logical shift
        logic [1:0] temp = inB[1:0];
        while(temp!=0) begin
            if (inB[2]) begin
              {rslt,sc_o} = {'b0,inA}
            end
            else begin
              {sc_o,rslt} = {inA,'b0}
            end
          temp--;
        end
      end
      3'b111: // and
        rslt = inA & inB;
    endcase
  end
  
end
   
endmodule