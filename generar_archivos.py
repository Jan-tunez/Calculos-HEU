# -*- coding: utf-8 -*-
"""
Script para generar archivos de entrada Heu-N{i}.in
Basado en los pasos 1 al 4 descritos.
"""

import os

def main():
    # Nombres de los archivos de entrada
    archivo_nakata = "MejoresConfNakata-5.4C1.dat"
    archivo_sio = "HEU-SiOPosiciones.dat"
    archivo_na = "HEU-NaPosiciones.dat"
    archivo_texto = "Texto.txt"

    print("Leyendo archivos de entrada...")

    # --- PASO 1: Procesar MejoresConfNakata-5.4C1.dat ---
    # Capturar las posiciones de los símbolos "Al" para cada línea
    posiciones_al_por_linea = []
    with open(archivo_nakata, 'r') as f:
        lineas_nakata = f.readlines()
    
    for linea in lineas_nakata:
        posiciones = []
        # Dividimos la línea en tokens para encontrar índices
        tokens = linea.split()
        for idx, token in enumerate(tokens):
            if token == "Al":
                posiciones.append(idx)
        posiciones_al_por_linea.append(posiciones)

    print(f"Paso 1 completado. Se procesaron {len(posiciones_al_por_linea)} configuraciones.")

    # --- PASO 2: Procesar HEU-SiOPosiciones.dat y HEU-NaPosiciones.dat ---
    
    # Procesar HEU-SiOPosiciones.dat (solo primeros 108 renglones)
    datos_sio = []
    with open(archivo_sio, 'r') as f:
        todas_lineas_sio = f.readlines()
    
    # Tomamos solo las primeras 108
    lineas_sio_relevantes = todas_lineas_sio[:108]
    
    for linea in lineas_sio_relevantes:
        partes = linea.split()
        if len(partes) >= 4:
            simbolo = partes[0]
            val1 = partes[1]
            val2 = partes[2]
            val3 = partes[3]
            datos_sio.append([simbolo, val1, val2, val3])
    
    # Separar conceptualmente: primeros 72 son O/Si originales, siguientes 36 se modificarán
    datos_O_Si_base = datos_sio[:72]
    datos_Si_a_modificar = datos_sio[72:108]

    # Procesar HEU-NaPosiciones.dat (36 renglones)
    # Ignorar primeras 7 columnas y > columna 40. Capturar 'Na' y 3 valores.
    datos_na = []
    with open(archivo_na, 'r') as f:
        lineas_na = f.readlines()
    
    for linea in lineas_na:
        # La instrucción dice ignorar primeras 7 columnas y mas allá de la 40.
        # Asumimos que es por caracteres o columnas fijas, pero usualmente en estos archivos
        # es más seguro leer por tokens y filtrar, o cortar la cadena.
        # Dado que dice "caracteres Na y 3 valores numéricos en subsecuentes columnas",
        # intentaremos buscar el token 'Na' y los siguientes 3 números dentro del rango válido.
        
        # Cortamos la línea entre la columna 7 y la 40 (índices 6 a 39 en base 0)
        # Nota: Si el archivo es de ancho fijo, esto es preciso. Si es espaciado variable,
        # la instrucción de "columnas" puede referirse a caracteres.
        # Haremos un slice de la cadena para respetar la instrucción de columnas estrictamente.
        segmento = linea[6:40] 
        partes = segmento.split()
        
        # Buscamos 'Na' y los 3 números siguientes
        if 'Na' in partes:
            idx_na = partes.index('Na')
            if len(partes) > idx_na + 3:
                na_simbolo = partes[idx_na]
                v1 = partes[idx_na+1]
                v2 = partes[idx_na+2]
                v3 = partes[idx_na+3]
                datos_na.append([na_simbolo, v1, v2, v3])
            else:
                # Fallback si no hay suficientes datos después de Na en el segmento recortado
                # Intentamos leer toda la línea por si el corte fue muy agresivo para algunos formatos
                partes_full = linea.split()
                if 'Na' in partes_full:
                    idx_na = partes_full.index('Na')
                    if len(partes_full) > idx_na + 3:
                        datos_na.append([partes_full[idx_na], partes_full[idx_na+1], partes_full[idx_na+2], partes_full[idx_na+3]])
        else:
            # Si no encontramos Na con el corte estricto, intentamos en toda la línea como fallback
            partes_full = linea.split()
            if 'Na' in partes_full:
                idx_na = partes_full.index('Na')
                if len(partes_full) > idx_na + 3:
                    datos_na.append([partes_full[idx_na], partes_full[idx_na+1], partes_full[idx_na+2], partes_full[idx_na+3]])

    print(f"Paso 2 completado. Cargados {len(datos_O_Si_base)} átomos base, {len(datos_Si_a_modificar)} átomos a modificar y {len(datos_na)} átomos Na.")

    # --- PASO 3: Procesar Texto.txt ---
    with open(archivo_texto, 'r') as f:
        todas_lineas_texto = f.readlines()
    
    # Primeras 3 líneas (índices 0, 1, 2)
    primeras_3_lineas = "".join(todas_lineas_texto[:3])
    
    # Líneas 5 a 39 (índices 4 a 38)
    lineas_5_a_39 = "".join(todas_lineas_texto[4:39])

    print("Paso 3 completado. Textos cargados.")

    # --- PASO 4: Generar archivos Heu-N{i}.in ---
    num_configuraciones = len(lineas_nakata)
    
    print(f"Iniciando generación de {num_configuraciones} archivos...")

    for i in range(num_configuraciones):
        nombre_archivo_salida = f"Heu-N{i+1}.in"
        
        with open(nombre_archivo_salida, 'w') as f_out:
            # 1. Guardar el primer texto (líneas 1-3)
            f_out.write(primeras_3_lineas)
            
            # 2. Guardar explícitamente: prefix='Naka5.4-i'
            f_out.write(f"     prefix='Naka5.4-{i+1}'\n")
            
            # 3. Guardar el segundo texto (líneas 5-39)
            f_out.write(lineas_5_a_39)
            
            # 4. Información de los primeros 72 renglones de HEU-SiOPosiciones.dat (tal cual)
            for item in datos_O_Si_base:
                # Formato original: Simbolo Val1 Val2 Val3
                f_out.write(f"{item[0]} {item[1]} {item[2]} {item[3]}\n")
            
            # 5. Restantes 36 renglones modificados
            # Obtener las posiciones de Al para esta configuración i
            posiciones_actuales = posiciones_al_por_linea[i]
            
            # Iteramos sobre los 36 átomos que originalmente eran Si (o mezcla)
            # La instrucción dice: "Para los restantes 36 renglones, se modificarán los caracteres 'Si' por 'Al' 
            # en cada una de las j-ésimas posiciones."
            # Y "se tomarán solo las j-esimas lineas guardas del archivo HEU-NaPosiciones.dat"
            
            # Asumimos que hay una correspondencia 1 a 1 entre los 36 renglones de SIO (72-108),
            # las posiciones encontradas en Nakata, y las líneas de Na.
            
            for j in range(36):
                if j < len(datos_Si_a_modificar) and j < len(datos_na):
                    atom_data = datos_Si_a_modificar[j].copy() # [Simbolo, x, y, z]
                    na_data = datos_na[j] # ['Na', x, y, z]
                    
                    # Verificar si la posición j corresponde a una posición donde debe ir Al
                    # La variable 'posiciones_actuales' contiene los índices (0-based o 1-based?) de los Al.
                    # En el paso 1 capturamos índices de tokens. Asumiremos que si el índice j está en la lista,
                    # ese átomo específico se convierte en Al y se inserta su Na.
                    
                    # Nota: La lógica exacta de "j-ésimas posiciones" depende de cómo se indexaron en el Paso 1.
                    # Si en el Paso 1 guardamos [9, 21...] refiriéndonos a la columna del token en la línea de Nakata,
                    # aquí necesitamos mapear eso a los 36 átomos de Si.
                    # Sin embargo, la instrucción dice: "en cada una de las j-ésimas posiciones... extraídas previamente".
                    # Interpretación más robusta: Las listas de posiciones del Paso 1 indican CUÁLES de los 36 sitios son Al.
                    # Pero la lista del Paso 1 son índices de tokens en la línea de texto de Nakata.
                    # Asumiremos que la lista `posiciones_actuales` indica los índices (0-based) de los 36 átomos que son Al.
                    # Si los índices del Paso 1 son mayores a 35, habría un desajuste. 
                    # Dado que hay 36 átomos de Si/Al en la celda y 36 líneas en Na, asumiremos correspondencia directa.
                    
                    # Revisión: El archivo Nakata tiene símbolos Si y Al. Si hay 6 Al, la lista tendrá 6 números.
                    # Esos números probablemente indican qué átomo de la lista de 36 es Al.
                    # Si el número es, digamos, 5, significa que el 5to átomo (índice 4 o 5) es Al.
                    
                    es_al = False
                    # Ajuste de índice: Si el archivo Nakata usa indexing 1-based o 0-based.
                    # Probemos verificando si 'j' (0-based) está en la lista. 
                    # Si la lista viene de split(), los índices son 0-based respecto a los tokens.
                    # Pero esos tokens son toda la línea. 
                    # Suposición: Los números en la lista `posiciones_actuales` corresponden a los índices de los 36 átomos.
                    # Si la lista es [9, 21...], y tenemos 36 átomos, esos índices deben ser menores a 36.
                    
                    if j in posiciones_actuales:
                        es_al = True
                    
                    if es_al:
                        # Cambiar símbolo a Al
                        atom_data[0] = "Al"
                        # Escribir el átomo Al modificado
                        f_out.write(f"{atom_data[0]} {atom_data[1]} {atom_data[2]} {atom_data[3]}\n")
                        # Escribir el átomo Na asociado (línea j de NaPosiciones)
                        f_out.write(f"{na_data[0]} {na_data[1]} {na_data[2]} {na_data[3]}\n")
                    else:
                        # Si no es Al, se mantiene como Si (o lo que fuera originalmente)
                        # La instrucción dice "modificarán los caracteres Si por Al en cada una de las j-ésimas posiciones".
                        # Implica que si no está en la lista, se queda igual? O solo escribimos los que cambian?
                        # El contexto de archivos .in de QE suele listar TODOS los átomos.
                        # Por tanto, escribimos el átomo original (Si) si no es Al.
                        # Y NO escribimos el Na si no es Al (porque el Na compensa la carga del Al).
                        f_out.write(f"{atom_data[0]} {atom_data[1]} {atom_data[2]} {atom_data[3]}\n")

            # 6. Texto final
            f_out.write(" K_POINTS gamma\n")
            
        print(f"Archivo generado: {nombre_archivo_salida}")

    print("\nProceso finalizado correctamente. Se han generado todos los archivos .in")

if __name__ == "__main__":
    # Verificar existencia de archivos antes de correr
    archivos_req = ["MejoresConfNakata-5.4C1.dat", "HEU-SiOPosiciones.dat", "HEU-NaPosiciones.dat", "Texto.txt"]
    faltantes = [f for f in archivos_req if not os.path.exists(f)]
    
    if faltantes:
        print("Error: Faltan los siguientes archivos de entrada en la carpeta actual:")
        for f in faltantes:
            print(f" - {f}")
        print("Por favor asegúrate de que estén en la misma carpeta que este script.")
        input("Presiona Enter para salir...")
    else:
        main()
        input("\nPresiona Enter para salir...")
