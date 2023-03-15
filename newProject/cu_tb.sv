module cu_tb;
	reg [3:0] instr;
	logic RegDst, Branch, MemRead, 
     MemtoReg, MemWrite, ALUSrc, RegWrite;
	
	Control ctl1(.instr,
	  .RegDst  , 
	  .Branch  , 
	  .MemRead,
	  .MemtoReg,
	  .MemWrite , 
	  .ALUSrc   , 
	  .RegWrite );
	
	initial begin
	#100 //lw
	instr = 4'b0110;
	#100 //sw
	instr = 4'b1000;
	#100 //set
	instr = 4'b1101;
	#100;	//bne 1
	instr = 4'b1100;
	#100;	// bne 0
	instr = 4'b1100;
	#100;	//add
	instr = 4'b0000;
	#100; //mov
	instr = 4'b0010;
	#100; //xor
	instr = 4'b0100;
	#100; // lsl 1
	instr = 4'b1010;
	#100; // lsl 2
	instr = 4'b1011;
	#100; // lsl 3
	instr = 4'b1011;
	#100; //lsr 1
	instr = 4'b1010;
	#100;	//lsr 2
	instr = 4'b1010;
	#100;	//lsr 3
	instr = 4'b1010;
	#100;
	end

endmodule