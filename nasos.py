class nasos:
    def __init__(self,stream11,stream12,water,KPDnasos,water_streams):
        self.KPDnasos = KPDnasos
        self.P0  = water_streams.at[stream11,'P']
        self.P1  = water_streams.at[stream12,'P']
        
        self.H0 = water_streams.at[stream11,'H']
        self.G  = water_streams.at[stream11,'G']
        self.water=water
        self.T0 = self.water.p_h(self.P0,self.H0)['T']
    def calc(self):
        self.s1teor = self.water.p_t(self.P0,self.T0)['s']
        self.h1teornasos = self.water.p_s(self.P1,self.s1teor)['h']
        self.h1realnasos = self.water.p_t(self.P0,self.T0)['h']+(self.h1teornasos-self.water.p_t(self.P0,self.T0)['h'])/self.KPDnasos
        self.T1nasosCO2=self.water.p_h(self.P1,self.h1realnasos)['T']
        Rabota = self.G*(self.h1realnasos - self.water.p_t(self.P0,self.T0)['h'])
        return [self.T1nasosCO2,self.P1,self.h1realnasos,self.G,Rabota]