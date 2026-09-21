import cocotb 
from cocotb.clock import Clock 
from cocotb.triggers import RisingEdge
from cocotb.triggers import Timer
import zlib
with open('../../tools/symbol_table.mem') as f:
    table = [int(line.strip(), 16) for line in f]
def expected_index(ticker):
        v = int.from_bytes(ticker.ljust(8, b' '), 'big')
        return table[zlib.crc32(v.to_bytes(8, 'big')) & 0x1FFFF]
@cocotb.test()
async def test_symbol_lookup(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    dut.data_in.value = int.from_bytes(b'MU'.ljust(8, b' '), 'big')
    dut.in_valid.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    assert dut.symbol_index.value == expected_index(b'MU'), f"MU: got {int(dut.symbol_index.value)}"
    assert dut.out_valid.value == 1
    dut.data_in.value = int.from_bytes(b'NVDA'.ljust(8, b' '), 'big')
    dut.in_valid.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    assert dut.symbol_index.value == expected_index(b'NVDA'), f"NVDA: got {int(dut.symbol_index.value)}"
    dut.data_in.value = int.from_bytes(b'FND'.ljust(8, b' '), 'big')
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    assert dut.symbol_index.value == 0x3FF, f"FND should be untracked: got {hex(int(dut.symbol_index.value))}"

        