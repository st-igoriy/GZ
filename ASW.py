
import mat_properties as prop
import numpy as n
import pandas as pd


class Accum():
    def __init__(self, water, water_streams, accumulation, ASWatm, **kwargs):

        self._V = 1
        self._D = 1
        self._F = 1
        self._H = 1
        self._P_accum = 1e-1
        self._T_accum = 95
        self._D = 1
        self._kolichestvo = 1
        self._V = n.pi*self._D**3/4
        self._F = 1.5*n.pi*self._D**2
        self._khi = 1
        self._lambda_min_vata = 0.045
        self.delta_min_vata = 0.01

        self._water = water
        self.water_streams = water_streams
        self.accumulation = accumulation
        self.ASWatm=ASWatm

        self._T_nar_vozd = self.water_streams.at['AIR', 'T']

        if 'stream11' in kwargs.keys():
            self._stream11 = kwargs['stream11']
        if 'stream12' in kwargs.keys():
            self._stream12 = kwargs['stream12']
        if 'stream_obratnoi_setevoi_vody' in kwargs.keys():
            self._stream_obratnoi_setevoi_vody = kwargs['stream_obratnoi_setevoi_vody']
        if 'stream_pryamoi_setevoi_vody' in kwargs.keys():
            self._stream_pryamoi_setevoi_vody = kwargs['stream_pryamoi_setevoi_vody']
        if 'T_nar_vozd' in kwargs.keys():
            self._T_nar_vozd = kwargs['T_nar_vozd']

        self._T_obr_set_voda = self.water_streams.at[self._stream_obratnoi_setevoi_vody, 'T']
        self._P_obr_set_voda = self.water_streams.at[self._stream_obratnoi_setevoi_vody, 'P']
        self._h_obr_set_voda = self._water.p_t(
            self._P_obr_set_voda, self._T_obr_set_voda)['h']
        self._G_obr_set_voda = self.water_streams.at[self._stream_obratnoi_setevoi_vody, 'G']
        self._f = 0
        self._T_accum = 0
        self._h_accum = 0
        self._P_accum = 0
        self._Mass = 0
        self._Q = 0

    def set_construct(self, **kwargs):

        if 'D' in kwargs.keys():
            self._D = kwargs['D']
        if 'd' in kwargs.keys():
            self._D = kwargs['d']
        if 'Diametr' in kwargs.keys():
            self._D = kwargs['Diametr']
        if 'kolichestvo' in kwargs.keys():
            self._kolichestvo = kwargs['kolichestvo']
        if 'Visota' in kwargs.keys():
            self._H = kwargs['Visota']
        if 'lambda_min_vata' in kwargs.keys():
            self._lambda_min_vata = kwargs['lambda_min_vata']
        if 'delta_min_vata' in kwargs.keys():
            self._delta_min_vata = kwargs['delta_min_vata']

        self._V = n.pi*self._D**2/4 * self._H
        self._F = n.pi*self._D*self._H + n.pi*self._D**2/2

        pass

    def zaryadka(self, tau):

        if self._f == 0:
            # тут уточнить
            self._T_accum = self.water_streams.at[self._stream_pryamoi_setevoi_vody, 'T']
#             self._h_accum = self.water_streams.at[self._stream_pryamoi_setevoi_vody,'H']# тут уточнить

            # тут уточнить
        
            if self.ASWatm == False:
                self._P_accum = self.water_streams.at[self._stream_pryamoi_setevoi_vody, 'P']
            else:
                self._P_accum = 0.1
                if self.water_streams.at[self._stream_pryamoi_setevoi_vody, 'T'] < 95:
                    self._T_accum = self.water_streams.at[self._stream_pryamoi_setevoi_vody, 'T']
                else:
                    self._T_accum = 95
            self._h_accum = self._water.p_t(self._P_accum, self._T_accum)['h']
            print(self._h_accum,'h_accum')
            print(self._P_accum,'self._P_accum')
            print(self._T_accum,'self._T_accum')
            self.water_streams.at[self._stream11, 'T'] = self._T_accum
            self.water_streams.at[self._stream11, 'H'] = self._h_accum
            self.water_streams.at[self._stream11, 'P'] = self._P_accum
            self._G = self._kolichestvo*self._V*self._water.p_t(self._P_accum, self._T_accum)['rho']/(tau*3600)
            self.water_streams.at[self._stream11, 'G'] = self._G
            self._Mass = self._kolichestvo*self._V * \
                self._water.p_t(self._P_accum, self._T_accum)['rho']
            self._Q = self._Mass * (self._h_accum - self._h_obr_set_voda)  # kJ
            self._f = 1
#             print(self._Q)
            self.accumulation.at["ASW", "Qw"] = self._Q/1000
            self.accumulation.at["ASW", "T"] = self._T_accum
        else:
            print("Аккумулятор заполнен")
        return {'T_accum': self._T_accum, 'Q': self._Q, 'G': self._G}

    def razryadka(self, tau):
        if self._f == 1:
            self.water_streams.at[self._stream12, 'T'] = self._T_accum
            self.water_streams.at[self._stream12, 'H'] = self._h_accum
            self.water_streams.at[self._stream12, 'P'] = self._P_accum
            self._G = self._Mass/(tau*3600)
            self.water_streams.at[self._stream12, 'G'] = self._G
            self._f = 0
            self.water_streams.at[self._stream11, 'T'] = 0
            self.water_streams.at[self._stream11, 'H'] = 0
            self.water_streams.at[self._stream11, 'P'] = 0
            self.water_streams.at[self._stream11, 'G'] = 0
            self._Q = 0
            self.accumulation.at["ASW", "Qw"] = self._Q/1000
            self.accumulation.at["ASW", "T"] = self._T_accum
        else:
            print("Аккумулятор пустой")

            self.water_streams.at[self._stream11, 'T'] = 0
            self.water_streams.at[self._stream11, 'H'] = 0
            self.water_streams.at[self._stream11, 'P'] = 0
            self.water_streams.at[self._stream11, 'G'] = 0
        return {'T_accum': self._T_accum, 'h_accum': self._h_accum, 'P_accum': self._P_accum, 'G': self._G, }

    def jdat(self,time):
        self._poteri = time*3600/1000*3.14*self._H*(self._T_accum-self._T_nar_vozd)/(1/2*self._lambda_min_vata*n.log((self._D+2*self._delta_min_vata)/self._D)+1/(100000*self._D)+1/(20*(self._D+2*self._delta_min_vata)))+ time*3600/1000*2*3.14*self._D**2/4*(self._T_accum-self._T_nar_vozd)/(1/20+1/100000+self._delta_min_vata/self._lambda_min_vata) #kJ
 
        self._Q = self._Q - self._poteri   
        self._h_accum = self._Q/self._Mass + self._water.p_t(self._P_obr_set_voda, self._T_obr_set_voda)['h']
        self._T_accum = self._water.p_h(self._P_accum, self._h_accum)['T']     
        self.water_streams.at[self._stream11,'T'] = "None"
        self.water_streams.at[self._stream11,'H'] = "None"
        self.water_streams.at[self._stream11,'P'] = "None"
        self.water_streams.at[self._stream11,'G'] = "None"  
        return {'T_accum': self._T_accum, 'poteri': self._poteri, 'Q': self._Q}
    
    def jdat_n(self,tau):
        for i in range(100):
            self.jdat(tau/100)
        pass
   