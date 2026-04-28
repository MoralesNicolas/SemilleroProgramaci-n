import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import Config
from src.models.student import Student
from src.generators.pdf_generator import PDFGenerator
from src.processors.omr_processor import OMRProcessor
from src.utils.csv_handler import CSVHandler


def ask_path(message, required=True):
    path = input(message).strip()
    if required and (not path or not os.path.exists(path)):
        print("Ruta inválida")
        return None
    return path if path else None


def generate():
    print("Generación de hojas")

    csv_path = ask_path("CSV con cédulas: ")
    if not csv_path:
        return

    try:
        num_questions = int(input("Número de preguntas: ").strip() or 0)
    except:
        print("Número inválido")
        return

    header = ask_path("Imagen encabezado (opcional): ", required=False)
    if header and not os.path.exists(header):
        header = None

    title = input("Título [HOJA DE RESPUESTAS]: ").strip() or "HOJA DE RESPUESTAS"
    footer = input("Footer [ICFES]: ").strip() or "ICFES"
    output = input("Ruta de salida PDF: ").strip()

    ids = CSVHandler.read_student_ids(csv_path)
    students = [Student(i) for i in ids]

    generator = PDFGenerator(Config(), header, title, footer)
    generator.generate_sheets(students, num_questions, output)

    print(f"PDF generado: {output} | Estudiantes: {len(students)}")


def process():
    print("Lectura de hojas")

    pdf_path = ask_path("PDF escaneado: ")
    if not pdf_path:
        return

    try:
        num_questions = int(input("Número de preguntas: ").strip() or 0)
    except:
        print("Número inválido")
        return

    output = input("Ruta de salida CSV: ").strip()

    processor = OMRProcessor(Config())
    results = processor.process_pdf(pdf_path)

    CSVHandler.write_responses(output, results, num_questions)

    print(f"CSV generado: {output} | Hojas procesadas: {len(results)}")


def main():
    Config.ensure_dirs()

    while True:
        print("1 Generar hojas")
        print("2 Procesar hojas")
        print("3 Salir")

        option = input("Seleccione opción: ").strip()

        if option == "1":
            generate()
        elif option == "2":
            process()
        elif option == "3":
            break
        else:
            print("Opción inválida")


if __name__ == "__main__":
    main()