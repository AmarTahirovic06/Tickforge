import cocotb
from cocotb.triggers import Timer
import zlib
@cocotb.test()
async def test_crc_matches_zlib(dut):
    for ticker in [b'MU', b'NVDA', b'APPL', b'VEEV']:
        v = int.from_bytes(ticker.ljust(8, b' '), 'big') 
        dut.data_in.value = v 
        await Timer(1, unit="ns")
        expected = zlib.crc32(ticker.ljust(8, b' '))
        assert dut.crc_out.value == expected, f"{ticker}: got {hex(dut.crc_out.value)} want {hex(expected)}"
        
 
