import pathlib
from PIL import Image
from collections import Counter
import os

# --- CONFIGURACIÓN ---
# 1. ¡IMPORTANTE! Cambia esta línea por la ruta a tu carpeta principal.
#    Usa la barra '/' incluso en Windows.
#    Ejemplo: "D:/Proyectos/mi_dataset"
#    Ejemplo: "C:/Users/TuUsuario/Desktop/fotos_proyecto"

RUTA_DATASET = pathlib.Path("D:/Universidad Continental/202502/Construcción de Software/Unidad 3/Reconocimiento Facial/dataset"
)

# 2. Define qué extensiones de archivo buscar
extensiones_validas = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
# ---------------------


# Contadores e inicializadores
conteo_clases = Counter()
conteo_formatos = Counter()
total_ancho = 0
total_alto = 0
total_imagenes = 0
archivos_invalidos = []

print(f"--- 📊 Iniciando análisis de: {RUTA_DATASET} ---")

# Usamos rglob() para buscar recursivamente en todas las subcarpetas
for ruta_archivo in RUTA_DATASET.rglob('*.*'):
    
    # Comprobar si es un formato de imagen válido
    if ruta_archivo.suffix.lower() in extensiones_validas:
        total_imagenes += 1
        
        # 1. Contar por clase (asume que la clase es la carpeta padre)
        # ej: .../persona_A/img_01.jpg -> la clase es 'persona_A'
        nombre_clase = ruta_archivo.parent.name
        conteo_clases[nombre_clase] += 1
        
        # 3. Contar formato
        conteo_formatos[ruta_archivo.suffix.lower()] += 1
        
        # 2. Obtener dimensiones
        try:
            with Image.open(ruta_archivo) as img:
                ancho, alto = img.size
                total_ancho += ancho
                total_alto += alto
        except Exception as e:
            print(f"  Error al leer {ruta_archivo.name}: {e}")
            archivos_invalidos.append(ruta_archivo.name)
            total_imagenes -= 1 # No la contamos si falla
            conteo_clases[nombre_clase] -= 1
            conteo_formatos[ruta_archivo.suffix.lower()] -= 1

# --- Impresión del Reporte ---

if total_imagenes == 0:
    print("\n¡ERROR! No se encontraron imágenes válidas en la ruta especificada.")
    print("Verifica tu variable 'RUTA_DATASET'.")
else:
    # 1. Cantidad de imágenes - Total y por clase
    print(f"\n## 1. Cantidad de Imágenes (Total: {total_imagenes}) ##")
    for clase, conteo in conteo_clases.items():
        print(f"  - Clase '{clase}': {conteo} imágenes")

    # 4. Balance de clases
    print("\n## 2. Balance de Clases ##")
    if len(conteo_clases) > 1:
        min_imgs = min(conteo_clases.values())
        max_imgs = max(conteo_clases.values())
        print(f"  - Imágenes por clase: Mínimo={min_imgs}, Máximo={max_imgs}")
        if (max_imgs / min_imgs) > 1.8: # Umbral de desbalanceo (ej. > 80% dif)
            print("  - ¡Advertencia! El dataset parece estar desbalanceado.")
        else:
            print("  - El dataset está razonablemente balanceado.")
    else:
        print("  - Solo se encontró una clase, no se puede evaluar balance.")

    # 2. Dimensiones promedio
    print("\n## 3. Dimensiones Promedio ##")
    avg_ancho = total_ancho / total_imagenes
    avg_alto = total_alto / total_imagenes
    print(f"  - Tamaño promedio: {avg_ancho:.0f} x {avg_alto:.0f} px (Ancho x Alto)")

    # 3. Formato
    print("\n## 4. Consistencia de Formato ##")
    for formato, conteo in conteo_formatos.items():
        print(f"  - {formato}: {conteo} archivos")
    if len(conteo_formatos) > 1:
        print("  - ¡Advertencia! Se encontraron múltiples formatos.")
    else:
        print("  - Buena consistencia: Todas las imágenes tienen el mismo formato.")

    if archivos_invalidos:
        print("\n## Errores ##")
        print(f"  - {len(archivos_invalidos)} archivos no pudieron leerse (corruptos?):")
        for f in archivos_invalidos[:5]: # Muestra los primeros 5
            print(f"    - {f}")


# 5. Condiciones de captura
print("\n## 5. Condiciones de Captura (Análisis Manual) ##")
print("  - Este análisis debe ser visual.")
print("  - Abre la carpeta y revisa una muestra de imágenes.")
print("  - Busca variaciones en: Iluminación (sombras), Fondo (complejidad) y Pose (frontal, perfil, etc.).")

print("\n--- ✅ Análisis completado ---")