from modules.fileManagement import readConfig, writeLog
from modules.testTracking import TestTracker
from modules.bashFlags import getFlagObj
from modules.apiIF import deviceInterface

if __name__ == "__main__":
    testLog = []
    args = getFlagObj()
    cfg = readConfig("config.json")

    try:
        devIF = deviceInterface(cfg["settings"])
        if cfg == None:
            raise Exception(f"{args.configPath} file not found.")

        tracker = TestTracker(len(cfg["tests"]))
        tableHeader = "[itr/ttl]  Data name                                           Adr:Num  Type        Expected(Modbus)                Received(SSH)                   Status"
        tableSep    = '-'*len(tableHeader)

        print(TestTracker.wrapColor(f"Testing {devIF.model}:", "BOLD"))
        print(tableHeader)
        print(tableSep)
        for itrReg, (name, obj) in enumerate(cfg["tests"].items(), 1):
            adr, cc, rpr = obj["adr"], obj["cc"], obj["rpr"]
            rsp, exp, status = devIF.testReg(adr, cc, rpr, obj["cmnd"])
            msg, color = tracker.incCount(status)
            testLog.append(', '.join(map(str, [name, adr, cc, rpr, exp.replace(',', ' '), str(rsp).replace(',', ' '), msg])) + '\n')

            print(f"[{itrReg:>3}/{tracker.total:>3}]  {name:<50}  {adr:0>3}:{cc:0>3}  {rpr:<10}  {rsp:<30}  {exp:<30}  {TestTracker.wrapColor(msg, color):<6}")
            print(tracker.getResults())
            print(tracker.rmLines(), end="")
        print(tableSep)
        print(tracker.getResults())
    except Exception as e:
        print(TestTracker.wrapColor(f"Error: {e}", "WARNING", "BOLD"))
    else:
        print(TestTracker.wrapColor(f"\nTest's completed succesfully.", "BOLD"))
    finally:
        try:
            filePath, fileName = writeLog(args.outputPath, devIF.model, testLog)
            print("Done. Output file location:", filePath)
        except Exception as e:
            print(TestTracker.wrapColor(f"Error: Failed to write output file: {e}", "WARNING", "BOLD"))
        print("Exiting...")

    

    

    