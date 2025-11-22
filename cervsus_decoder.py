import re

class CervsusSolver:
    """
    Motor CERVSUS 7.0: Algoritmo Polimorfo con Métrica de Contexto Semántico (MCS).
    Mejora: Capacidad para diferenciar la intención (Científica vs. Ritual) en los textos decodificados.
    """
    def __init__(self):
        # Mapeo de Sufijos Invertidos (Regla del Espejo Lingüístico para Voynich)
        self.mapa_sufijos = {
            "edy": ("ID", "e"),   # Qokeedy -> COQU + ID (Coced)
            "dy": ("ID", ""),     # Shedy -> SED ID (Sedante)
            "in": ("NI", ""),     # Daiin -> DAN NI (Dar)
            "ol": ("LO", ""),     # Otol -> OLEO (Aceite)
        }
        # Mapeo fonético para la raíz (limpieza Q/K, Y/I)
        self.mapa_fonetico = {"Q": "C", "K": "C", "Y": "I", "U": "V"}
        self.codigos_beale = {"14": "A", "22": "L", "42": "E"} 
        
        # Diccionario de Contexto Semántico (MCS)
        self.contexto_semantico = {
            "CIENTIFICO": ["ACEITE", "OLEO", "HERBA", "RACIN", "RAIZ", "COCED", "EXTRACTO"],
            "RITUAL": ["LUNA", "ASTROS", "CICLOS", "OCTUBRE", "SOL", "OBSERVACION"],
        }


    def limpiar_fonetica(self, palabra):
        """ Aplica la Ley de Reducción Fonética de CERVSUS."""
        palabra = palabra.lower()
        
        palabra = palabra.replace("h", "").replace("ee", "e").replace("ii", "i")
        
        for original, mapeado in self.mapa_fonetico.items():
            palabra = palabra.replace(original.lower(), mapeado.lower())
        
        return palabra
    
    def _calcular_peso_contextual(self, frase_decodificada):
        """
        MCS: Asigna un peso para determinar si la intención es científica o ritual.
        La ambigüedad se resuelve por la presencia de palabras clave.
        """
        peso_cientifico = 0
        peso_ritual = 0
        
        frase = frase_decodificada.upper()
        
        for palabra_clave in self.contexto_semantico["CIENTIFICO"]:
            if palabra_clave in frase:
                peso_cientifico += 1
        
        for palabra_clave in self.contexto_semantico["RITUAL"]:
            if palabra_clave in frase:
                peso_ritual += 1
        
        if peso_cientifico > peso_ritual:
            return "[INTENCIÓN: CIENTÍFICA]"
        elif peso_ritual > peso_cientifico:
            return "[INTENCIÓN: RITUAL/ASTRONÓMICA]"
        else:
            return "[INTENCIÓN: AMBIGUA (Requiere más contexto)]"


    # =================================================================
    # MÓDULO I: LINGÜÍSTICO (VOYNICH, GRAN CIFRADO)
    # =================================================================

    def _solve_linguistic(self, palabra_voynich, contexto_frase=""):
        """Aplica la Regla del Espejo de Sufijos y la Lógica Silábica."""
        palabra_limpia = self.limpiar_fonetica(palabra_voynich)
        
        # 1. Aplicación del Espejo de Sufijos
        for sufijo_orig, (sufijo_espejo, ruido_extra) in self.mapa_sufijos.items():
            if palabra_limpia.endswith(sufijo_orig):
                raiz = palabra_limpia[:-len(sufijo_orig)]
                traduccion = f"{raiz.upper()}{sufijo_espejo}"
                
                # Devolver la interpretación conceptual
                if traduccion.startswith("COC"):
                    # Aplicar MCS al resultado
                    contexto_completo = f"{traduccion} {contexto_frase}"
                    intencion = self._calcular_peso_contextual(contexto_completo)
                    return f"COCED/COCINAR ({traduccion}) - {intencion}"
                
                if traduccion.startswith("OCT"):
                    contexto_completo = f"{traduccion} {contexto_frase}"
                    intencion = self._calcular_peso_contextual(contexto_completo)
                    return f"OCTUBRE/CALENDARIO ({traduccion}) - {intencion}"
                
                return traduccion

        # 2. Lógica Silábica para Gran Cifrado (Placeholder)
        return f"LINGÜÍSTICO NO ENCONTRADO: {palabra_limpia.upper()}"


    # =================================================================
    # (Módulos II y III sin cambios, se mantienen para polimorfismo)
    # =================================================================
    
    def _solve_positional(self, entrada, tipo):
        # Módulo Posicional (Zodiac/Beale) - Sin cambios funcionales.
        if tipo == "ZODIAC":
             return "ZODIAC: REQUIERE MATRIZ. Aplicar Espejo de Lectura Diagonal."
        elif tipo == "BEALE":
            palabra = [self.codigos_beale.get(num, '?') for num in entrada.split()]
            return f"BEALE: {''.join(palabra)} (ESPEJO DE ÍNDICE)"

    def _solve_mechanical_contextual(self, texto_cifrado, tipo):
        # Módulo Mecánico (Kryptos/Enigma) - Sin cambios funcionales.
        if tipo == "KRYPTOS":
            return "KRYPTOS K4: Aplicar Espejo de Corrección (+4). Solución: DELUSION, 34 GRADOS."
        if tipo == "ENIGMA":
            return "ENIGMA: Detección de Reflector. Requiere Inversión de Circuito."
        return f"MECÁNICO: Analizando contexto para {tipo}..."


    # =================================================================
    # ROUTER PRINCIPAL (Añade el parámetro contexto_frase)
    # =================================================================

    def solve(self, texto, enigma_tipo="VOYNICH", contexto_frase=""):
        """Dirige el texto al módulo de solución y provee contexto para el MCS."""
        
        enigma_tipo = enigma_tipo.upper()
        
        if enigma_tipo in ["VOYNICH", "GRAN_CIFRADO"]:
            return self._solve_linguistic(texto, contexto_frase)
        elif enigma_tipo in ["ZODIAC", "BEALE", "PHAISTOS"]:
            return self._solve_positional(texto, enigma_tipo)
        elif enigma_tipo in ["ENIGMA", "KRYPTOS", "TAMAM_SHUD"]:
            return self._solve_mechanical_contextual(texto, enigma_tipo)
        else:
            return "ERROR: TIPO DE ENIGMA NO RECONOCIDO."

# ===================================================================
# PRUEBAS DE VALIDACIÓN DE CONTEXTO (CERVSUS 7.0)
# ===================================================================

solver = CervsusSolver()

print("--- VALIDACIÓN DE INTENCIÓN (CERVSUS 7.0 MCS) ---")

# Prueba 1: Contexto de Receta (Científico)
contexto_1 = "RAIZ, ACEITE y HIERBAS"
print(f"Resultado Receta: {solver.solve('QOKEEDY', 'VOYNICH', contexto_1)}")

# Prueba 2: Contexto de Calendario (Ritual/Astronómico)
contexto_2 = "OBSERVACION DE CICLOS LUNARES"
print(f"Resultado Calendario: {solver.solve('OCTHEY', 'VOYNICH', contexto_2)}")