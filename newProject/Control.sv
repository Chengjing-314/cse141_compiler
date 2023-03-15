// control decoder
module Control #(parameter mcodebits = 4)(
  input [mcodebits-1:0] instr,    // subset of machine code (any width you need)
  output logic RegDst, Branch, MemRead, 
     MemtoReg, MemWrite, ALUSrc, RegWrite);	   // for up to 8 ALU operations

 logic [2:0] firstThree;
always_comb begin
// defaults
  RegDst 	=   'b0;   // 1: not in place  just leave 0
  Branch 	=   'b0;   // 1: branch (jump)
  MemRead = 'b0;
  MemWrite  =	'b0;   // 1: store to memory
  ALUSrc 	=	'b0;   // 1: immediate  0: second reg file output
  RegWrite  =	'b1;   // 0: for store or no op  1: most other operations 
  MemtoReg  =	'b0;   // 1: load -- route memory instead of ALU to reg_file data in
// sample values only -- use what you need

	firstThree	= instr[3:1];
  if (firstThree == 3'b110) begin
    case(instr)
      'b1100: begin //bne
        ALUSrc = 'b0;
        Branch = 'b1;
        RegWrite = 'b0;
      end
      'b1101: begin //set
        ALUSrc = 'b1;
        RegWrite = 'b1;
      end
    endcase

  end else begin
    case(firstThree)    // override defaults with exceptions
      'b000:  begin					// add
        RegDst = 'b1;       
          end
      'b001: begin               // mov
        RegDst = 'b1;  
      end
      'b010:  begin               // xor
        RegDst = 'b0; 
      end
      'b011:  begin				  // load
      MemtoReg = 'b1;    // 
      ALUSrc = 'b0;
      MemRead = 'b1;
      RegDst = 'b1;
          end
      'b100:  begin				  // store
      ALUSrc = 'b0;
      MemWrite = 'b1;
		RegWrite = 'b0;
          end
      'b101:  begin					// logical shift
        RegDst = 'b1;        
          end
      'b111:  begin               // and
        RegDst = 'b0; 
      end
    // ...
    endcase
  end


end
	
endmodule