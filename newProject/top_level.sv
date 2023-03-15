// sample top level design
module top_level(
  input        clk, reset, req,
  output logic done);
  parameter D = 12,             // program counter width
    A = 3;             		  // ALU command bit width
  wire[D-1:0] target, 			  // jump 
              prog_ctr;
  wire        RegWrite;
	wire[3:0] instr;
  wire[7:0]   datA,datB,              regfile_dat,
			         rslt,               // alu output
               muxB;		  // from RegFile
  wire [2:0]  muxA, muxD; 
  wire [4:0] immediate;

  logic sc_in,   				  // shift/carry out from/to ALU
			sc_o,
   		pariQ,              	  // registered parity flag from ALU
		zeroQ;                    // registered zero flag from ALU 
  logic[7:0] dat_out;
  logic [7:0] value;
  logic [1:0] addr_lut;
  wire  relj;                     // from control to PC; relative jump enable
  wire  pari,
			pcSrc,
        zero,
		sc_clr,
		RegDst,
		MemtoReg,
		MemRead,
		sc_en,
        MemWrite,
        ALUSrc;		              // immediate switch
  wire[3:0] alu_cmd;
  wire[2:0] shift_value;
  wire[8:0]   mach_code;          // machine code
  wire[2:0] rd_addrA, rd_addrB;    // address pointers to reg_file
// fetch subassembly
  PC #(.D(D)) 					  // D sets program counter width
     pc1 (.reset            ,
         .clk              ,
		 .absjump_en (pcSrc),
		 .target           ,
		 .prog_ctr          );

  assign rd_addrA = mach_code[2:0];
  assign rd_addrB = mach_code[5:3];
  assign alu_cmd  = mach_code[8:5];
  assign immediate = mach_code[4:0];
  assign instr = mach_code[8:5];
  assign shift_value = mach_code[2:0];

// lookup table to facilitate jumps/branches
  PC_LUT #(.D(D))
    pl1 (.addr_lut(immediate)  ,
         .target          );   
			  
// contains machine code
  instr_ROM ir1(.prog_ctr,
               .mach_code);  

// control decoder
  Control ctl1(.instr,
  .RegDst, 
  .Branch  (absj)  , 
  .MemRead,
  .MemWrite , 
  .ALUSrc   , 
  .RegWrite   ,     
  .MemtoReg);
  
	// lookup table to facilitate jumps/branches
  PC_LUT_2
    pl2 (.index(immediate)  ,
         .value          );
  assign muxA = RegDst ? rd_addrB :3'b000;
  assign muxD = absj ? 3'b000 : rd_addrB;
  reg_file #(.pw(3)) rf1(.dat_in(regfile_dat),	   // loads, most ops
              .clk         ,
              .wr_en   (RegWrite),
              .rd_addrA(rd_addrA),
              .rd_addrB(muxD),
              .wr_addr (muxA),      // in place operation
              .datA_out(datA),
              .datB_out(datB)); // rb = rd

  assign muxB = ALUSrc? value : datA;

  alu alu1(.alu_cmd,
         .inA    (datB),
		 .inB    (muxB),
		 .sc_i   (sc_in),   // output from sc register
     .shift_value,
		 .rslt       ,
		 .sc_o  , // input to sc register
		 .pari,
     .zero  );  // check for zero/zeroQ here

  assign pcSrc = absj & zero;
  dat_mem dm1(.dat_in(datB)  ,  // from reg_file
             .clk           ,
			 .wr_en  (MemWrite), // stores
			 .addr   (datA),
             .dat_out);
  assign regfile_dat = MemtoReg ? dat_out : rslt;
// registered flags from ALU
  always_ff @(posedge clk) begin
    pariQ <= pari;
	zeroQ <= zero;
    if(sc_clr)
	  sc_in <= 'b0;
    else if(sc_en)
      sc_in <= sc_o;
  end

  assign done = prog_ctr == 256;
 
endmodule