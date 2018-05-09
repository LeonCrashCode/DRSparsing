from DRS import DRS as DRS

def CanTypeChanging

def proc(self):
                if self.supertag[0] == "lam" and type(self.supertag[3]) == types.ListType and self.supertag[3][0] == "drs" and len(self.supertag) == 4:
                        self.supertag[3][2] = [self.supertag[3][1], "", "$x0$"] + self.supertag[3][2]
                        self.supertag[3][3] = self.change_b(self.supertag[3][3], "$v1$", "$x0$")
                        self.supertag[3] = ["merge", "", self.supertag[3], ["app", "", "$v1$", "$x0$"]]

        def type_changing_2(self):
                if self.supertag[0] == "lam" and type(self.supertag[3]) == types.ListType and self.supertag[3][0] == "drs" and len(self.supertag) == 4:
                        self.supertag[3][2] = [self.supertag[3][1], "", "$x0$"] + self.supertag[3][2]
                        self.supertag[3][3] = self.change_b(self.supertag[3][3], "$v1$", "$x0$")
                        self.supertag[3] = ["alfa", "", "def", self.supertag[3], ["app", "", "$v1$", "$x0$"]]

        def type_changing_3(self):
                if self.supertag[0] == "lam" and type(self.supertag[3]) == types.ListType and self.supertag[3][0] == "sdrs" and len(self.supertag) == 4:
                        self.supertag[3] = self.change_b(self.supertag[3], "$v1$", "$x0$")
                        self.flag = False
                        self.supertag = self.type_changing_3_left_proc(self.supertag)
                        self.flag = False
                        self.supertag = self.type_changing_3_right_proc(self.supertag)
