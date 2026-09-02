S_LEN = 0
S_BODY = 1
import cocotb 
from cocotb.clock import Clock 
from cocotb.triggers import RisingEdge
from cocotb.triggers import Timer

@cocotb.test()   
async def test_framer_finds_boundaries(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    await Timer(1, unit="ns")
    dut.rst_n.value = 0
    dut.valid.value = 0
    await (RisingEdge(dut.clk))
    await Timer(1, unit="ns") 
    assert dut.state.value == S_LEN, f"Expected S_LEN after reset, got {dut.state.value}"
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    dut.valid.value = 1 
    stream = [0x00, 0x03, 0x50, 0xAA, 0xBB,
        0x00, 0x03, 0x41, 0xCC, 0xDD,
        0x00, 0x02, 0x50, 0xEE]
    expected = [S_LEN, S_BODY, S_BODY, S_BODY, S_LEN, S_LEN, S_BODY, S_BODY, S_BODY, S_LEN, S_LEN, S_BODY, S_BODY, S_LEN]
    expected_trade = [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1]
    for i,(byte, exp, exp_trade) in enumerate(zip(stream, expected, expected_trade)):
        dut.data_in.value = byte
        await RisingEdge(dut.clk)
        await Timer(1, unit="ns")
        assert dut.state.value == exp, f"byte{i} (0x{byte:02X}): is_trade_expected {exp_trade}, expected {exp}, got {dut.state.value}"
    

