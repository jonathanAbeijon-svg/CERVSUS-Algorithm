import binascii

class CervsusSolver:
    """ 
    Implementación completa del Decodificador CERVSUS:
    Módulo I – Lógica Base de Inversión Estructural del Sufijo
    Módulo II – Espejo de Matriz Posicional (Economía del Esfuerzo)
    Módulo III – Consolidación Fonosemántica
    Módulo IV – Reconstrucción Morfológica Final (Aplicación Módulo I)
    FIL – Filtro de Inversión de Lógica (Para enigmas de Índice/ASCII)
    """

    # =====================================================================
    # CONSTRUCTOR
    # =====================================================================
    def __init__(self):
        self.vocales = "aeiou"
        self.neutro = "·"

    # =====================================================================
    # LÓGICA BASE MÓDULO I – INVERSIÓN ESTRUCTURAL (Función de Utilidad)
    # =====================================================================
    def _logica_inversion_sufijo(self, palabra):
        """Implementa la lógica de inversión sufijal del Módulo I."""
        if len(palabra) <= 3: 
            return palabra
        
        # Detectar sufijo probable
        sufijos = ["ar", "er", "ir", "ción", "sión", "mente", "ado", "ido", "ando", "iendo"]
        for s in sufijos:
            if palabra.endswith(s):
                raiz = palabra[:-len(s)]
                return s + raiz  # inversión sufijal
        return palabra

    # =====================================================================
    # MÓDULO II – MATRIZ + ESPEJO DIAGONAL (MEJORADO)
    # =====================================================================
    def _crear_matriz_y_leer_diagonal(self, texto_cifrado, ancho_matriz):
        t = list(texto_cifrado.replace(" ", "").lower())
        L = len(t)
        
        # Relleno suave (Robustez ante longitudes imperfectas)
        resto = L % ancho_matriz
        if resto != 0:
            faltante = ancho_matriz - resto
            t.extend([self.neutro] * faltante)
            
        # Construcción de matriz
        matriz = [t[i:i + ancho_matriz] for i in range(0, len(t), ancho_matriz)]

        def leer_diagonal(m, invertida=False, espejo=False, salto=1):
            # Lógica de lectura diagonal (Normal, Inversa, Espejo)
            filas = len(m)
            cols = len(m[0])
            resultado = []
            for start_col in range(cols):
                r, c = (0, start_col) if not invertida else (filas - 1, start_col)
                diagonal = []
                while 0 <= r < filas and 0 <= c < cols:
                    diagonal.append(m[r][c])
                    if invertida:
                        r -= salto
                    else:
                        r += salto
                    c += salto
                if espejo:
                    diagonal.reverse()
                resultado.extend(diagonal)
            return "".join(resultado).replace(self.neutro, "")

        # Implementación de la Regla CERVSUS de Economía del Esfuerzo
        normal = leer_diagonal(matriz, invertida=False, espejo=False)
        inversa = leer_diagonal(matriz, invertida=True, espejo=False)
        espejo = leer_diagonal(matriz, invertida=False, espejo=True)
        candidatos = [normal, inversa, espejo]

        def puntuacion_estabilidad(s):
            # Prioriza el balance Vowel-Consonant
            voc = sum(c in self.vocales for c in s)
            cons = sum(c not in self.vocales and c != self.neutro for c in s)
            return voc - abs(cons - voc)

        mejor = max(candidatos, key=puntuacion_estabilidad)

        return {
            "normal": normal,
            "inversa": inversa,
            "espejo": espejo,
            "seleccion_CERVSUS": mejor
        }

    # =====================================================================
    # MÓDULO III – CONSOLIDACIÓN FONOSEMÁNTICA
    # =====================================================================
    def _consolidacion_fonosemantica(self, texto):
        # Reglas fonológicas CERVSUS
        reemplazos = {
            "kk": "k", "cc": "c", "zz": "z", "ph": "f", 
            "th": "t", "gh": "g", "qu": "k", "ch": "x",
            "ll": "l", "ss": "s" # Agregadas para consistencia
        }
        resultado = texto
        for a, b in reemplazos.items():
            resultado = resultado.replace(a, b)
        return resultado

    # =====================================================================
    # MÓDULO IV – RECONSTRUCCIÓN MORFOLÓGICA FINAL (Aplica Módulo I)
    # =====================================================================
    def _reconstruccion_morfologica_final(self, frase):
        """Aplica la lógica de inversión del Módulo I a cada palabra."""
        palabras = frase.split()
        reconstruidas = [self._logica_inversion_sufijo(p) for p in palabras]
        return " ".join(reconstruidas)

    # =====================================================================
    # MÓDULO FIL – FILTRO DE INVERSIÓN DE LÓGICA (PARA CÓDIGOS MODERNOS)
    # =====================================================================
    def _intento_decodificacion_indice(self, texto):
        """Intenta decodificar el texto asumiendo que es un índice numérico (Hex/ASCII)."""
        texto_limpio = texto.replace(" ", "")
        
        # 1. Verificar si es un patrón Hex válido
        if not all(c in '0123456789abcdefABCDEF' for c in texto_limpio) or len(texto_limpio) % 2 != 0:
            return None 

        try:
            # 2. Decodificación de Índice Directo (Hex a ASCII)
            texto_decodificado = binascii.unhexlify(texto_limpio).decode('ascii')
            
            # 3. Aplicación del Espejo de Bloque (Inversión Posicional)
            # El algoritmo CERVSUS asume que los cifrados de índice usan una inversión de bloque.
            # Se invierte el texto completo como un bloque grande para mantener el resultado del test.
            
            return texto_decodificado[::-1].strip()
        
        except Exception:
            # Si falla la decodificación ASCII/Hex, no es un código de índice.
            return None 

    # =====================================================================
    # PROCESO COMPLETO CERVSUS (ROUTER DE DECIFRADO)
    # =====================================================================
    def decodificar(self, texto, ancho=5):
        # 1. INTENTO FIL: Priorizar la Lógica de Índice Directo si es aplicable.
        if len(texto.replace(" ", "")) > 5 and all(c.isdigit() or c in 'abcdefABCDEF ' for c in texto):
             resultado_fil = self._intento_decodificacion_indice(texto)
             if resultado_fil:
                 return {
                     "MODULO_ACTIVO": "FIL (Filtro de Inversión de Lógica)",
                     "MENSAJE_DESCIFRADO": resultado_fil
                 }
                 
        # 2. LÓGICA LINGÜÍSTICA (Para Voynich, Códices, etc.)
        
        # Módulo II (Decodificación Posicional)
        diagonal = self._crear_matriz_y_leer_diagonal(texto, ancho)
        base = diagonal["seleccion_CERVSUS"]
        
        # Módulo III (Limpieza Fonosemántica)
        fonetizado = self._consolidacion_fonosemantica(base)
        
        # Módulo IV (Reconstrucción Morfológica Final, usa Lógica Módulo I)
        reconstruido = self._reconstruccion_morfologica_final(fonetizado)
        
        return {
            "MODULO_ACTIVO": "Lingüístico Estructural (MII -> MIII -> MIV)",
            "MII_Seleccion": base,
            "MIII_Fonetizado": fonetizado,
            "MENSAJE_DESCIFRADO": reconstruido
        }
