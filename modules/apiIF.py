import time
from datetime import datetime
from paramiko import SSHClient, AutoAddPolicy
from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder


class deviceInterface:
    def __init__(self, cfg, timeout=10):
        self.model   = cfg["model"]
        self.timeout = timeout

        self.id = cfg["modbus"]["id"]
        self.modbus = ModbusTcpClient(cfg["modbus"]["ip"], cfg["modbus"]["port"])
        self.modbus.connect()

        self.ssh = SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        self.ssh.connect(hostname = cfg["ssh"]["ip"],
                         port     = cfg["ssh"]["port"],
                         username = cfg["ssh"]["user"],
                         password = cfg["ssh"]["pasw"])

        if self.model != self.SendSSHCommand("uci get system.system.routername"): 
            raise Exception("Device names do not match")


    def __del__(self):
        self.modbus.close()
        self.ssh.close()


    def SendSSHCommand(self, cmnd):
        i, o, e = self.ssh.exec_command(cmnd, timeout=self.timeout)
        return self.stripData(o.read().decode())


    def ReadReg(self, adr, cc, rpr):
        rsp = self.modbus.read_holding_registers(adr, cc, self.id)
        try:
            dat = rsp.registers
            decoder = BinaryPayloadDecoder.fromRegisters(dat, byteorder=Endian.Big)
            match rpr:
                case "int8":
                    #return decoder.decode_8bit_int()
                    return '.'.join([str(int(f'{dat[0]:016b}{dat[1]:016b}'[i:i+8], 2)) \
                                     for i in range(0, 32, 8)])
                case "uint16":
                    return decoder.decode_16bit_uint()
                    #return dat[0]
                case "int32":
                    return decoder.decode_32bit_int()
                    #return dat[1] if dat[0] == 0 else ~dat[0] + dat[1]
                case "uint32":
                    return decoder.decode_32bit_uint()
                    #return dat[0]*65536 + dat[1]
                case "uint32 (s)":
                    m = (dat[0]*65536 + dat[1]) // 60
                    return f"{m} min" if m < 60 else "{0}:{1:0>2}".format(*divmod(m, 60))
                case "float32":
                    return "{:.6f}".format(decoder.decode_32bit_float()) 
                case "unixts":
                    return dat[0]*1000
                case "date (s)":
                    ts = datetime.timestamp(datetime.strptime(self.stripData(decoder.decode_string(size=32).decode()), "%Y-%m-%d %H:%M:%S")) 
                    return ts if ts > 0 else 0
                case "str" | "date" | "unixts (s)":
                    return self.stripData(decoder.decode_string(size=32).decode())
                    # output = ""
                    # for el in dat:
                    #     hh = hex(el)[2:]
                    #     if hh != "0":
                    #         output += chr(int(hh[:2], 16)) + chr(int(hh[2:], 16))
                    # return self.stripData(output)
                case _:
                    return "Type not implemented"
        except:
            return rsp
        

    @staticmethod
    def stripData(dat):
        output = str(dat).strip('\x00').strip('\t').replace('\n', '').strip(' ')
        return output if output != "" else "0"
    

    def testReg(self, adr, cc, rpr, cmnd):
        rsp = self.ReadReg(adr, cc, rpr)
        exp = "-"
        try:
            match rsp.exception_code:
                case  1: rsp = "Illegal Function"
                case  2: rsp = "Illegal Data Address"
                case  3: rsp = "Illegal Data Value"
                case  4: rsp = "Slave Device Failure"
                case  5: rsp = "Acknowledge"
                case  6: rsp = "Slave Device Busy"
                case  7: rsp = "Negative Acknowledge"
                case  8: rsp = "Memory Parity Error"
                case 10: rsp = "Gateway Path Unavailable"
                case 11: rsp = "Gateway Target Device Failed to Respond"
                case  _: rsp = "Err" 
        except:        
            exp = self.SendSSHCommand(cmnd) if cmnd != "" else "Err: no command"
            if exp == "ERROR: Couldn't retrieve data":
                status = -1
            else:
                status = str(rsp) in exp
        else:
            status = -1
        finally:
            time.sleep(0.1)

        return rsp, exp, status


# dat = [35480, 23362]
# import struct
# value = struct.unpack('f', struct.pack('>HH', *dat))[0]
# print(value)
# rpr = "".join([f'{dat[0]:04x}{dat[1]:04x}'[i:i+2] \
#         for i in range(0, 8, 2)][::-1])
# print(rpr)
# byyyt = f'{int(rpr, 16):032b}'
# half1, half2 = byyyt[:23], byyyt[24:]
# print(byyyt)
# output1 = 0.0
# output2 = 0.0
# for p, b in enumerate(half1, 1):
#     print(1/(2**p))
#     output1 += int(b)*(1/(2**p))
# print(output1)
# for p, b in enumerate(half2, 1):
#     print(1/(2**p))
#     output2 += int(b)*(1/(2**p))
# print(output2*100+ output1-127)
# exit()
#devIF = deviceInterface(cfg["settings"], cfg["modbusSetup"])



# klausima
# curr active sim card slot
# mobile data visokius