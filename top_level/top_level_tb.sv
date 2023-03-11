module top_level_tb;
	bit clk;
	bit reset;
	logic req;
	wire done;
	top_level DUT(.clk(clk),
					.reset(reset),
					.req(req),
					.done(done));
	
	always begin
	#50  clk = 1'b1;       // tic
	#50  clk = 1'b0;       // toc
	end
	
	
	initial begin
	reset = 1'b1;
	#100 reset = 1'b0;
	#10ns req = 1'b1;
	#10ns req = 1'b0;
	wait(done);
	$display("done");
	#10ns $stop;
	end

endmodule