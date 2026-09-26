import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
from cocotb.triggers import Timer


async def boot(dut):
    # Hold reset, release it, and settle. Returns with one counting edge taken.
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    dut.rst_n.value = 0
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    assert dut.count.value == 0, f"Counter should be 0 after reset, got {dut.count.value}"
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")


@cocotb.test()
async def test_counter_increment(dut):
    # boot has already taken the first counting edge, so count is 1 on entry.
    await boot(dut)
    for i in range(1, 11):
        assert dut.count.value == i, f"Counter should be {i}, got {dut.count.value}"
        await RisingEdge(dut.clk)
        await Timer(1, unit="ns")


@cocotb.test()
async def test_counter_wraps(dut):
    # Four bits: 15 must roll to 0 rather than saturate.
    await boot(dut)
    for _ in range(14):
        await RisingEdge(dut.clk)
        await Timer(1, unit="ns")
    assert dut.count.value == 15, f"Expected 15 before the wrap, got {dut.count.value}"
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    assert dut.count.value == 0, f"Expected wrap to 0, got {dut.count.value}"


@cocotb.test()
async def test_counter_reset_mid_run(dut):
    # Reset is synchronous, so it clears on the next edge, not immediately.
    await boot(dut)
    for _ in range(5):
        await RisingEdge(dut.clk)
        await Timer(1, unit="ns")
    assert dut.count.value == 6, f"Expected 6 before reset, got {dut.count.value}"
    dut.rst_n.value = 0
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")
    assert dut.count.value == 0, f"Reset should clear the count, got {dut.count.value}"
