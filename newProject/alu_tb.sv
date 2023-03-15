module alu_tb;
	reg [3:0] alu_cmd;
	reg [7:0] inA;
	reg [7:0] inB;
	logic [7:0] rslt;
	logic sc_o,
			sc_i,
			pari,
			zero;
	
	  alu alu1(.alu_cmd,
         .inA    ,
		 .inB   ,
		 .sc_i   ,
		 .rslt      ,
		 .sc_o   ,
		 .pari,
     .zero  );
	
	initial begin
	#100 //set
	alu_cmd = 4'b1101;
	inA = 8'b00000001;
	inB = 8'b00011110;
	sc_i = 'b0;	
	#100;	//bne 1
	alu_cmd = 4'b1100;
	inA = 8'b00000010;
	inB = 8'b00000010;
	sc_i = 'b0;	
	#100;	// bne 0
	alu_cmd = 4'b1100;
	inA = 8'b00000000;
	inB = 8'b00000010;
	sc_i = 'b0;	
	#100;	//add
	alu_cmd = 4'b0000;
	inA = 8'b00000010;
	inB = 8'b00000011;
	sc_i = 'b0;	
	#100; //mov
	alu_cmd = 4'b0010;
	inA = 8'b00000010;
	inB = 8'b00000001;
	sc_i = 'b0;	
	#100; //xor
	alu_cmd = 4'b0100;
	inA = 8'b00000010;
	inB = 8'b00000001;
	sc_i = 'b0;	
	#100; // lsl 1
	alu_cmd = 4'b1010;
	inA = 8'b00010000;
	inB = 8'b00000001;
	sc_i = 'b0;	
	#100; // lsl 2
	alu_cmd = 4'b1011;
	inA = 8'b00010000;
	inB = 8'b00000010;
	sc_i = 'b0;
	#100; // lsl 3
	alu_cmd = 4'b1011;
	inA = 8'b00010000;
	inB = 8'b00000011;
	sc_i = 'b0;	
	#100; //lsr 1
	alu_cmd = 4'b1010;
	inA = 8'b00010000;
	inB = 8'b00000101;
	sc_i = 'b0;	
	#100;	//lsr 2
	alu_cmd = 4'b1010;
	inA = 8'b00010000;
	inB = 8'b00000110;
	sc_i = 'b0;	
	#100;	//lsr 3
	alu_cmd = 4'b1010;
	inA = 8'b00010000;
	inB = 8'b00000111;
	sc_i = 'b0;
	#100;
	end

endmodule