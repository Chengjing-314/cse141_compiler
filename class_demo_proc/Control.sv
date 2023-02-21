// control decoder
module Control #(parameter opwidth = 2, mcodebits = 4)(
  input [mcodebits-1:0] instr,    // subset of machine code (any width you need)
  output logic RegDst, Branch, MemRead, 
     MemtoReg, MemWrite, ALUSrc, RegWrite,
  output logic[opwidth-1:0] ALUOp);	   // for up to 8 ALU operations

always_comb begin
  logic [2:0] firstThree = instr[3:1];
// defaults
  RegDst 	=   'b0;   // 1: not in place  just leave 0
  Branch 	=   'b0;   // 1: branch (jump)
  MemRead = 'b0;
  MemWrite  =	'b0;   // 1: store to memory
  ALUSrc 	=	'b0;   // 1: immediate  0: second reg file output
  RegWrite  =	'b1;   // 0: for store or no op  1: most other operations 
  MemtoReg  =	'b0;   // 1: load -- route memory instead of ALU to reg_file data in
  ALUOp	    =   'b111; // y = a+0;
// sample values only -- use what you need
  if (firstThree == 3'b110) begin
    case(instr)
      'b1100: begin //bne
        ALUop = 3'b001;
        ALUSrc = 'b0;
        Branch = 'b1;
        RegWrite = 'b0;
      end
      'b1101: begin //set
        ALUSrc = 'b1;
        RegWrite = 'b1;
        ALUOp = 'b011;
      end
    endcase

  end else begin
    case(firstThree)    // override defaults with exceptions
      'b000:  begin					// add
        RegDst = 'b1;
        ALUOp = 3'b010;        
          end
      'b001: begin               // mov
        RegDst = 'b1;
        ALUOp = 3'b010;  
      end
      'b010:  begin               // xor
        RegDst = 'b0;
        ALUOp = 3'b010;  
      end
      'b011:  begin				  // load
      MemtoReg = 'b1;    // 
      ALUSrc = 'b1;
      MemRead = 'b1;
          end
      'b100:  begin				  // store
      ALUSrc = 'b1;
      MemWrite = 'b1;
          end
      'b101:  begin					// logical shift
        RegDst = 'b1;
        ALUOp = 3'b010;        
          end
      'b111:  begin               // and
        RegDst = 'b1;
        ALUOp = 3'b010;  
      end
    // ...
    endcase
  end


end
	
endmodule