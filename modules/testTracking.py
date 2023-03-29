class TestTracker:
    bcod = {
        "OKGREEN"   : "\033[92m",
        "WARNING"   : "\033[93m",
        "ERRORRED"  : "\033[91m",
        "BOLD"      : "\033[1m",
        "ENDC"      : "\033[0m",
        "RMLINE"    : "\033[F",
        "MVBACK"    : "\033[K"
    }


    def __init__(self, _total):
        self.passed = 0
        self.errord = 0
        self.failed = 0
        self.total  = _total


    def incCount(self, status):
        match status:
            case -1:
                self.errord += 1
                return "ERROR", "WARNING"
            case 0:
                self.failed += 1
                return "FAILED", "ERRORRED"
            case 1:
                self.passed += 1
                return "PASSED", "OKGREEN"
            case _:
                return "Undefined result", "ERRORRED"
    
    
    def getResults(self):
        return self.wrapColor("Total results: ", "BOLD") + self.wrapColor(str(self.passed), "OKGREEN")  + "/" + \
               self.wrapColor(str(self.failed), "ERRORRED") + "/" + self.wrapColor(str(self.errord), "WARNING")


    @staticmethod
    def wrapColor(text, *colors):
        return "".join([TestTracker.bcod[c] for c in colors]) + text + TestTracker.bcod["ENDC"]
    

    @staticmethod
    def rmLines(cc=1):
        return (TestTracker.bcod["RMLINE"] + TestTracker.bcod["MVBACK"])*cc