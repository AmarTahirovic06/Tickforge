import cocotb 
from cocotb.clock import Clock 
from cocotb.triggers import RisingEdge
from cocotb.triggers import Timer

@cocotb.test()   
async def test_shift_reg_assembles_bytes(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await Timer(1, unit="ns")
    dut.rst_n.value = 0
    dut.valid.value = 0
    await (RisingEdge(dut.clk))
    await Timer(1, unit="ns") 
    assert dut.data_out.value == 0, f"Expected 0 after reset, got {hex(dut.data_out.value)}"
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    dut.data_in.value = 0x24
    dut.valid.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    dut.data_in.value = 0x36
    dut.valid.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    assert dut.data_out.value == 0x2436, f"got {hex(dut.data_out.value)}"
    dut.valid.value = 0
    assert dut.data_out.value == 0x2436 
    dut.data_in.value = 0x66
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    dut.data_in.value = 0x77 
    dut.valid.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    assert dut.data_out.value == 0x3677

