# -----------------------------------------------------------------------------
# Divisor Silábico em Python
# Autor: Thiago de Sousa Paiva
# Descrição: Algoritmo implementado para realizar a divisão silábica de palavras 
#            em português utilizando regras fonológicas. O código foi inspirado 
#            em métodos descritos no trabalho de pesquisa de Daniela Filipa Macedo 
#            Braga Moreira da Silva, focado em algoritmos para a divisão 
#            silábica automatizada.
# Fonte: https://ruc.udc.es/dspace/bitstream/handle/2183/1011/Braga_DanielaFilipaMacedoMoreiradaSilva_TD_2008.pdf
# -----------------------------------------------------------------------------

class Palavra:
    def __init__(self):
        self.p = ""
        self.grafemas = []
        self.silabas = []

    def set_palavra(self, palavra):
        self.p = palavra.strip().lower()
        self.grafemas = self.separar_grafemas()
        self.silabear()
        
    def espaco(self, c1):
        return c1 in [" ", "", None]
        
    def vogal(self, c1):
        return c1 in ["a", "e", "o", "i", "u", "á", "é", "ó", "ú", "í", "ã", "õ", "â", "ê", "ô", "à"]
    
    def glide(self, c1):
        return c1 in ["i", "u"]
    
    def consoante_nasal(self, c1):
        return c1 in ["m", "n"]
    
    def consoante_liquida(self, c1):
        return c1 in ["l", "r", "rr"]
    
    def consoante_fricativa(self, c1, c2 = ""):
        cons = ["f", "v", "s", "ç", "z", "j", "x"]
        cons_especiais = ["c", "g"]
        cons_digrafo = ["ss", "ch"]
        
        if c1 in cons:
            return True
        
        if c1 in cons_digrafo:
            return True
        
        if c2 != "":
            if c1 in cons_especiais and c2 in ["e" ,"i"]:
                return True
            
        return False
    
    def consoante_oclusiva(self, c1, c2 = ""):
        cons = ["p", "t", "b", "d"]
        cons_especiais = ["c", "g"]
        cons_digrafo = ["qu", "gu"]
        
        if c1 in cons:
            return True
        
        if c2 != "":
            if c1 in cons_especiais and c2 in ["a" ,"o","u"]:
                return True
            elif c1 in cons_digrafo and c2 in ["e" ,"i"]:
                return True
        
        return False
    
    def consoante(self, c1, c2 = ""):
        cons = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", 
                "n", "p", "q", "r", "s", "t", "v", "w", "x", "z"]
        cons_digrafo = ["lh", "nh"]
        
        if c1 in cons:
            return True
        
        if c1 in cons_digrafo:
            return True
            
        return self.consoante_oclusiva(c1,c2) or self.consoante_fricativa(c1,c2) or self.consoante_liquida(c1) or self.consoante_nasal(c1)

    def quantidade_de_silabas(self):
        return len(self.silabas)

    def tipo_de_palavra(self):
        n = len(self.silabas)
        if n == 1:
            return "Monossílaba"
        elif n == 2:
            return "Bisílaba"
        elif n == 3:
            return "Trissílaba"
        else:
            return "Polissílaba"

    def silaba(self, indice):
        if 1 <= indice <= len(self.silabas):
            return self.silabas[-indice]
        return ""
    
    def separar_grafemas(self):
        grafemas_lista = []
        cons_digrafo = ["nh", "lh", "ch"]
        cons_especiais = ["qu", "gu"]
        i = 0
        while i < len(self.p):
            gm0 = self.p[i] 
            gm1 = self.p[i + 1] if i + 1 < len(self.p) else ""
            gm2 = self.p[i + 2] if i + 2 < len(self.p) else ""
            
            if (gm0 + gm1 in cons_digrafo):
                grafemas_lista.append(gm0 + gm1)
                i += 2
                continue
            elif gm0 + gm1 in cons_especiais and gm2 in ["e" ,"i"]:
                grafemas_lista.append(gm0 + gm1)
                i += 2
            else:
                grafemas_lista.append(gm0)
                i += 1
                
            
        return grafemas_lista
 
    def silabear(self):
        self.silabas = []
        if not self.grafemas:
            return False

        i = 0
        i_silaba = 0
        s = ""
        
        while i < len(self.grafemas):
            ga2 = self.grafemas[i - 2] if i >= 2 else ""
            ga1 = self.grafemas[i - 1] if i >= 1 else ""
            gm0 = self.grafemas[i] 
            gm1 = self.grafemas[i + 1] if i + 1 < len(self.grafemas) else ""
            gm2 = self.grafemas[i + 2] if i + 2 < len(self.grafemas) else ""
            gm3 = self.grafemas[i + 3] if i + 3 < len(self.grafemas) else ""
            gm4 = self.grafemas[i + 4] if i + 4 < len(self.grafemas) else ""
            
            regra = 0
            caso = 0
                
            if not self.vogal(gm0):
                s += gm0
                i += 1
                i_silaba += 1
                continue
            
            # regra 5
            if (caso == 0 and i_silaba == 0 and self.vogal(gm0) 
            and (self.consoante(gm1,gm2))
            and (self.vogal(gm2) or self.consoante_liquida(gm2))):
                regra = 5 
                caso = 1
            
            # regra 3
            if (caso == 0 and i_silaba == 0 and self.vogal(gm0) 
            and (self.glide(gm1) or self.consoante_nasal(gm1) or gm1 in ["s", "r", "l", "x", "c"])
            and (self.consoante(gm2,gm3))):
                regra = 3 
                caso = 2
            
            # regra 1
            if ((caso == 0 and i_silaba == 0 and self.vogal(gm0)) 
            and (self.vogal(gm1))): 
                regra = 1
                caso = 1
                
            # regra 2
            if (caso == 0 and i_silaba == 0 and self.vogal(gm0) 
            and self.consoante(gm1,gm2) 
            and self.consoante(gm2,gm3) 
            and self.consoante_oclusiva(gm3,gm4)):
                regra = 2 
                caso = 5
                
            # regra 4
            if (caso == 0 and i_silaba == 0 and self.vogal(gm0) 
            and (self.consoante_oclusiva(gm1,gm2) or self.consoante_fricativa(gm1,gm2) or gm1 == "g")
            and (self.consoante_oclusiva(gm2,gm3) or self.consoante_nasal(gm2) or gm2 == "v")
            and self.vogal(gm3)):
                regra = 4 
                caso = 2
                           
            # regra 6
            if (caso == 0 and i_silaba != 0 and self.vogal(gm0) 
            and (self.consoante(ga1,gm0))
            and (self.consoante(gm1,gm2))
            and (self.vogal(gm2))):
                regra = 6 
                caso = 3
                
            # regra 7
            if (caso == 0 and (i_silaba != 0 and self.vogal(gm0)) 
            and (self.consoante(ga1,gm0))
            and (self.glide(gm1))
            and (gm2 == "r")
            and (self.consoante(gm3,gm4))):
                regra = 7 
                caso = 3
                
            # regra 8B
            if (caso == 0 and (i_silaba != 0 and self.vogal(gm0)) 
            and (self.consoante_oclusiva(ga2,ga1) or self.consoante_fricativa(ga2,ga1))
            and (self.consoante_liquida(ga1))
            and (self.consoante_nasal(gm1) or gm1 in ["s"])):
                regra = 8 
                caso = 9
                
            # regra 8
            if (caso == 0 and (i_silaba != 0 and self.vogal(gm0)) 
            and (self.consoante_oclusiva(ga2,ga1) or self.consoante_fricativa(ga2,ga1))
            and (self.consoante_liquida(ga1))
            and (self.consoante(gm1,gm2))):
                regra = 8 
                caso = 8
                
            # regra 9
            if (caso == 0 and (i_silaba != 0 and self.vogal(gm0)) 
            and (self.consoante(ga1,gm0))
            and (self.glide(gm1))
            and (gm2 == "s")
            and (self.consoante_oclusiva(gm3,gm4))):
                regra = 9 
                caso = 7
                
            # regra 10
            if (caso == 0 and (i_silaba != 0 and self.vogal(gm0)) 
            and (self.consoante(ga1,gm0))
            and (self.consoante_nasal(gm1))
            and (gm2 == "s")
            and (self.consoante_oclusiva(gm3,gm4))):
                regra = 10 
                caso = 7
            
            # regra 16
            if (caso == 0 and i_silaba != 0 and self.vogal(gm0) 
            and (self.vogal(gm1) and gm1 == gm0)):
                regra = 16 
                caso = 1

            # regra 17
            if (caso == 0 and i_silaba != 0 and self.vogal(gm0) 
            and (self.consoante(ga1,gm0))
            and (self.vogal(gm1))
            and (self.consoante_nasal(gm2))):
                regra = 17 
                caso = 3
                                                  
            # regra 11
            if (caso == 0 and (i_silaba != 0 and self.vogal(gm0)) 
            and (self.consoante(ga1,gm0) or self.glide(ga1))
            and (self.glide(gm1))
            and (self.consoante(gm2,gm3))):
                regra = 11 
                caso = 4
                
            # regra 12
            if (caso == 0 and i_silaba != 0 and self.vogal(gm0) 
            and (self.consoante(ga1,gm0))
            and (self.glide(gm1))
            and (self.vogal(gm2) or self.espaco(gm2))):
                regra = 12 
                caso = 4
                
            # regra 13
            if (caso == 0 and i_silaba != 0 and self.vogal(gm0) 
            and (self.consoante(ga2,ga1))
            and (self.glide(ga1))
            and (self.consoante(gm1,gm2))
            and (self.vogal(gm2))):
                regra = 13 
                caso = 3

            # regra 20
            if (caso == 0 and i_silaba != 0 and self.vogal(gm0) 
            and (self.consoante_oclusiva(gm1,gm2) or (gm1 in ["c","g"]))
            and (self.consoante_liquida(gm2))
            and (self.vogal(gm3))):
                regra = 20 
                caso = 3
                             
            # regra 14
            if (caso == 0 and i_silaba != 0 and self.vogal(gm0) 
            and (self.consoante(ga1,gm0))
            and (self.consoante_liquida(gm1) or self.consoante_nasal(gm1) or gm1 in ["s", "c"])
            and (self.consoante(gm2,gm3))
            and (self.vogal(gm3) or self.consoante_liquida(gm3))):
                regra = 14 
                caso = 4
                
            # regra 15
            if (caso == 0 and i_silaba != 0 and self.vogal(gm0) 
            and (self.consoante(ga1,gm0))
            and ((self.consoante_liquida(gm1) or self.consoante_nasal(gm1) or gm1 in ["i"])
            and (self.espaco(gm2) or gm2 in ["s"]))):
                regra = 15 
                caso = 6
                
            # regra 23
            if (caso == 0 and i_silaba != 0 and self.vogal(gm0) and gm0 in ["ã", "õ"]
            and (self.consoante(ga1,gm0))
            and ((gm1 in ["o", "e"])
            or (gm2 == "s"))):
                regra = 23 
                caso = 6
                
            # regra 18
            if (caso == 0 and i_silaba != 0 and self.vogal(gm0) 
            and (self.consoante(ga1,gm0))
            and (self.vogal(gm1))):
                regra = 18 
                caso = 3
                
            # regra 19
            if (caso == 0 and i_silaba != 0 and self.vogal(gm0) 
            and (self.consoante(ga1,gm0))
            and (self.vogal(gm1))
            and (self.consoante_nasal(gm2))
            and (self.consoante(gm3,gm4))):
                regra = 19 
                caso = 7
   
            # regra 21
            if (caso == 0 and i_silaba != 0 and self.vogal(gm0) and gm0 == "i"
            and (ga2 in ["á", "é", "í", "ó", "ú"])
            and (self.consoante(ga1,gm0))
            and (gm1 in ["a", "o"])):
                regra = 21 
                caso = 6
            
            # regra 22
            if (caso == 0 and i_silaba != 0 and self.vogal(gm0) and gm0 == "i"
            and (self.consoante(ga1,gm0))
            and (gm1 in ["a", "o"])
            and (self.consoante(gm2,gm3) or gm2 == "i")):
                regra = 22 
                caso = 3
                
            print("regra: " + str(regra)+" caso: " + str(caso)+" "+ str(s) +" "+ str(gm0))    
            match caso:
                case 1:
                    s += gm0
                    i += 1
                    self.silabas.append(s)
                    i_silaba = 0
                    s = ""
                case 2:
                    s += gm0 + gm1
                    i += 2
                    self.silabas.append(s)
                    i_silaba = 0
                    s = ""
                case 3: 
                    s += gm0
                    i += 1
                    self.silabas.append(s)
                    i_silaba = 0
                    s = ""
                case 4:
                    s += gm0 + gm1
                    i += 2
                    self.silabas.append(s)
                    i_silaba = 0
                    s = ""
                case 5:
                    s += gm0 + gm1 + gm2
                    i += 3
                    self.silabas.append(s)
                    i_silaba = 0
                    s = ""
                case 6:
                  
                    while i < len(self.grafemas):
                        s += self.grafemas[i] 
                        i += 1

                    self.silabas.append(s)
                    i_silaba = 0
                    s = ""
                case 7:
                    s += gm0 + gm1 + gm2
                    i += 3
                    self.silabas.append(s)
                    i_silaba = 0
                    s = ""
                case 8:
                    s += gm0
                    i += 1
                    self.silabas.append(s)
                    i_silaba = 0
                    s = ""
                case 9:
                    s += gm0 + gm1
                    i += 2
                    self.silabas.append(s)
                    i_silaba = 0
                    s = ""
                case _:
                    while i < len(self.grafemas):
                        s += self.grafemas[i] 
                        i += 1

                    self.silabas.append(s)
                    i_silaba = 0
                    s = ""
                    continue
        if len(s)>0:
            self.silabas.append(s)
        return True

def main():
    file = "palavras.txt"
    try:
        with open(file, "r", encoding="utf-8") as arquivo:
            palavras = arquivo.readlines()
        
        for entrada in palavras:
            entrada = entrada.strip()  
            if entrada:  
                palavra = Palavra()
                palavra.set_palavra(entrada)
                print("Palavra: " + entrada + " Sílabas:", " - ".join(palavra.silabas))
    except FileNotFoundError:
        print("Erro: O arquivo "+ file + " não foi encontrado.")

main()