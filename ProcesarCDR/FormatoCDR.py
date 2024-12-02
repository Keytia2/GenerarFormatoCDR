import os
import argparse

def process_cdr_file(input_file, output_file):
    try:
        # Listas para almacenar líneas procesadas
        lines_with_newline = []
        lines_without_newline = []
        
        # Leer el archivo original
        with open(input_file, 'r', encoding='utf-8') as file:
            # Saltar el encabezado
            next(file)
            
            # Procesar línea por línea
            for line in file:
                line = line.replace(',\\ ,', ',,')
                
                if line.endswith(',\n'):
                    lines_with_newline.append(line)
                else:
                    lines_without_newline.append(line)
        
        processed_with_newline = [
            line.strip() + ',,,,,,\n' for line in lines_with_newline
        ]
        processed_without_newline = [
            line.strip() + ',,,,,,\r' for line in lines_without_newline
        ]
        
        all_processed_lines = processed_with_newline + processed_without_newline
        
        with open(output_file, 'w', encoding='utf-8') as file:
            file.writelines(all_processed_lines)
        
        print(f"Procesado: {input_file} -> {output_file}")
    
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {input_file}.")
    except Exception as e:
        print(f"Error inesperado al procesar {input_file}: {str(e)}")

def process_all_files_in_folder(input_folder):
    if not os.path.isdir(input_folder):
        print(f"Error: La carpeta '{input_folder}' no existe.")
        return

    # Crear la carpeta de salida dentro de la misma carpeta de entrada
    output_folder = os.path.join(input_folder, "archivos_procesados")
    os.makedirs(output_folder, exist_ok=True)

    archivos_procesados = 0
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.txt'):
            input_file = os.path.join(input_folder, file_name)
            output_file = os.path.join(output_folder, f"procesado_{file_name}")
            process_cdr_file(input_file, output_file)
            archivos_procesados += 1

    if archivos_procesados > 0:
        print(f"\n{archivos_procesados} archivo(s) procesado(s).")
        print(f"Archivos procesados guardados en: {output_folder}")
    else:
        print("\nNo se encontraron archivos .txt en la carpeta proporcionada.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Procesar todos los archivos CDR en una carpeta.")
    parser.add_argument(
        "input_folder",
        type=str,
        nargs="?",
        default=None,
        help="Ruta de la carpeta con archivos .txt para procesar. Si no se proporciona, se solicitará al usuario."
    )
    
    args = parser.parse_args()

    if args.input_folder:
        input_folder = args.input_folder
    else:
        input_folder = input("Introduce la ruta de la carpeta que contiene los archivos .txt: ").strip()

    process_all_files_in_folder(input_folder)
    input("\nPresiona Enter para salir..")
