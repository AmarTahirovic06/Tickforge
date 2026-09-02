import cocotb 
from cocotb.clock import Clock 
from cocotb.triggers import RisingEdge

@cocotb.test()   
async def test_counter_increment(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    dut.rst_n.value = 0
    await (RisingEdge(dut.clk)) 
    await (RisingEdge(dut.clk))
    assert dut.count.value == 0, f"Counter should be 0 after reset, got {dut.count.value}"
    dut .rst_n.value = 1
    await RisingEdge(dut.clk)
    for i in range(0, 10):
        await RisingEdge(dut.clk)
        assert dut.count.value == i + 1, f"Counter should be {i + 1}, got {dut.count.value}"

