class Entities():
    def __init__(self,mapwidth):
        self.copter1 = [-10,mapwidth/2,self.copter1movement]

    def copter1movement(self):
        pass

class Mapdat(Entities):
    def __init__(self):
        Entities.__init__(self,0)
        self.map = [
            "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
            "P                            P",
            "P                            P",
            "P                  PPPPPPPPPPP",
            "P                            P",
            "PPPPPPPP                     P",
            "P                            P",
            "P                            P",
            "P                            P",
            "P                        PPPPP",
            "P                            P",
            "P                            P",
            "PPPPPPPPPPPPPPP              P",
            "P                            P",
            "P                            P",
            "P                            P",
            "P                   PPPPPPPPPP",
            "P                            P",
            "PPPPPP                       P",
            "P                            P",
            "P                            P",
            "P                            P",
            "P                            P",
            "P                            P",
            "P                      PPPPPPP",
            "PPPPP                        P",
            "P                            P",
            "P                            P",
            "P                 PPPPPPPPPPPP",
            "P                            P",
            "PPPPPPPPPP                   P",
            "P                            P",
            "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPP", ]

        self.entitydat = None

