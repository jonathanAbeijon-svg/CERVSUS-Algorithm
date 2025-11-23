import re

class CervsusUniversalEngine:
    """
    CERVSUS v10.0 - Motor Híbrido Universal
    ---------------------------------------
    Integración de protocolos mecánicos (v8.0) y lingüísticos contextuales (v9.1).
    Diseñado por Jonathan Abeijon.
    """

    def __init__(self):
        self.alfabeto = "abcdefghijklmnopqrstuvwxyz"
        
        # --- CONFIGURACIÓN MOTOR OMEGA (VOYNICH) ---
        # Diccionario Maestro de Raíces Latinas Técnicas (Validado)
        self.diccionario_voynich = {
            "QOK":  {"lat": "COC",  "sig": "COCINAR/DECOCTAR", "ctx": ["RECETA", "HERBAL"]},
            "SHED": {"lat": "SUD",  "sig": "SUDAR/VAPOR",      "ctx": ["BALNEOLOGIA", "BAÑOS"]},
            "CHOL": {"lat": "COL",  "sig": "COLAR/FILTRAR",    "ctx": ["FARMACIA", "RECETA"]},
            "OL":   {"lat": "OLE",  "sig": "ACEITE/ESENCIA",   "ctx": ["FARMACIA", "HERBAL"]},
            "OR":   {"lat": "ORO",  "sig": "ORAL/DORADO",      "ctx": ["FARMACIA"]},
            "DA":   {"lat": "DA",   "sig": "DAR/ADMINISTRAR",  "ctx": ["GENERAL", "RECETA"]},
            "OK":   {"lat": "AQL",  "sig": "AGUA/LÍQUIDO",     "ctx": ["BALNEOLOGIA", "ASTRONOMIA"]},
            "YK":   {"lat": "AC",   "sig": "TALLO/AGUJA",      "ctx": ["HERBAL"]},
            "SA":   {"lat": "SANI", "sig": "FLUIDO/SALUD",     "ctx": ["BALNEOLOGIA", "HERBAL"]},
            "POL":  {"lat": "PUL",  "sig": "POLVO",            "ctx": ["RECETA", "FARMACIA"]},
            "FACH": {"lat": "FAC",  "sig": "HÁGASE",           "ctx": ["RECETA"]}
        }
        
        # Mapa de Inversión de Sufijos (Morfología)
        self.mapa_sufijos = {
            "EDY": "DO", "Y": "A", "AL": "LA", "IN": "NI", 
            "IIN": "NI", "OR": "RO", "YS": "S", "TON": "NOT"
        }

    # =========================================================================
    # UTILIDADES COMPARTIDAS
    # =========================================================================
    def _calcular_estabilidad(self, texto):
        """Métrica heurística: ¿Parece lenguaje natural?"""
        if not texto: return -100
        vocales = sum(1 for c in texto if c in "aeiou")
        consonantes = sum(1 for c in texto if c in "bcdfghjklmnpqrstvwxyz")
        # Penaliza si no hay equilibrio (MDI)
        return vocales - abs(consonantes - vocales)

    # =========================================================================
    # PROTOCOLO A: UNIVERSAL (Motor Alpha - Mecánica v8.0)
    # =========================================================================
    def _motor_alpha_mecanico(self, texto):
        """Analiza cifrados de rotación y sustitución simple."""
        
        # 1. Intento de Rotación Dinámica (César 1-25)
        mejor_score = -999
        mejor_texto = ""
        mejor_shift = 0
        
        for shift in range(1, 26):
            candidato = ""
            for char in texto.lower():
                if char in self.alfabeto:
                    idx = (self.alfabeto.index(char) + shift) % 26
                    candidato += self.alfabeto[idx]
                else:
                    candidato += char
            
            score = self._calcular_estabilidad(candidato)
            if score > mejor_score:
                mejor_score = score
                mejor_texto = candidato
                mejor_shift = shift
        
        # Umbral de seguridad Universal
        if mejor_score < -2:
            return f"FALLO: Ruido estadístico. Posible cifrado complejo o ruido."
            
        return f"ÉXITO (Rotación +{mejor_shift}): {mejor_texto} (Estabilidad: {mejor_score})"

    # =========================================================================
    # PROTOCOLO B: VOYNICH (Motor Omega - Lingüística v9.1)
    # =========================================================================
    def _analisis_morfologico(self, palabra):
        """Separa Raíz y Sufijo Voynich."""
        palabra = palabra.upper().strip()
        mejor_match = None
        match_len = 0
        
        for raiz in self.diccionario_voynich.keys():
            if palabra.startswith(raiz):
                if len(raiz) > match_len:
                    match_len = len(raiz)
                    mejor_match = raiz
        
        if mejor_match:
            return mejor_match, palabra[len(mejor_match):]
        
        return None, None

    def _triangulacion_visual(self, datos_raiz, contexto_usuario):
        """MÓDULO VII - Verifica la coherencia del significado con la imagen."""
        contextos_validos = datos_raiz["ctx"]
        
        if "GENERAL" in contextos_validos:
            return True, "VALIDADO (Contexto Universal)"
            
        if contexto_usuario.upper() in contextos_validos:
            return True, f"VALIDADO (Coincide con {contexto_usuario})"
            
        return False, f"ALERTA DE INCONSISTENCIA: La palabra es '{datos_raiz['sig']}' pero el contexto es '{contexto_usuario}'."

    def _motor_omega_voynich(self, palabra, contexto_visual):
        """Analiza Voynich usando la morfología inversa y la Triangulación."""
        
        raiz_v, sufijo_v = self._analisis_morfologico(palabra)
        
        if not raiz_v:
            return "FALLO: Raíz desconocida en Diccionario Maestro."

        sufijo_lat = self.mapa_sufijos.get(sufijo_v, sufijo_v[::-1])
        
        datos = self.diccionario_voynich[raiz_v]
        reconstruccion = f"{datos['lat']}{sufijo_lat}"

        validado, mensaje_validacion = self._triangulacion_visual(datos, contexto_visual)

        if not validado:
            return f"RECHAZADO POR TRIANGULACIÓN: {mensaje_validacion}"

        return f"ÉXITO: {datos['sig']} ({reconstruccion}) - {mensaje_validacion}"

    # =========================================================================
    # ROUTER PRINCIPAL (DISPATCHER)
    # =========================================================================
    def decodificar(self, entrada, modo="UNIVERSAL", contexto_visual=None):
        """
        Selector de Protocolos: Encapsula el conocimiento de CERVSUS.
        """
        print(f"\n--- EJECUTANDO CERVSUS v10.0 | MODO: {modo} ---")
        
        if modo == "UNIVERSAL":
            return self._motor_alpha_mecanico(entrada)
        
        elif modo == "VOYNICH":
            if not contexto_visual:
                return "ERROR: El modo VOYNICH requiere un 'contexto_visual' (Ej: RECETA, BAÑOS) para evitar alucinaciones."
            return self._motor_omega_voynich(entrada, contexto_visual)
        
        else:
            return "ERROR: Modo desconocido."
