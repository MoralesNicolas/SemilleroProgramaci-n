
class Clientes:
    def __init__(self, cedula, nombre, foto, celular, maleta):
        self._cedula = cedula
        self._nombre = nombre
        self._foto = foto
        self._celular = celular
        self._maleta = maleta

    def get_cedula(self):
        return self._cedula

    def get_maleta(self):
        return self._maleta

    def get_nombre(self):
        return self._nombre

    def get_foto(self):
        return self._foto

    def get_celular(self):
        return self._celular


class Reservas:
    def __init__(self, cliente, sector, carro, horario, maleta):
        self._cliente = cliente
        self._sector = sector
        self._carro = carro
        self._horario = horario
        self._maleta = maleta

    def get_cliente(self):
        return self._cliente

    def get_carro(self):
        return self._carro

    def get_sector(self):
        return self._sector

    def get_horario(self):
        return self._horario

    def get_maleta(self):
        return self._maleta

    def guardar_json(self, archivo):
        import json, os
        reservas = []
        if os.path.exists(archivo):
            with open(archivo, "r", encoding="utf-8") as f:
                try:
                    reservas = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    reservas = []
        reservas.append({
            "carro": self._carro,
            "cedula": self._cliente.get_cedula(),
            "nombre": self._cliente.get_nombre(),
            "horario": self.get_horario(),
            "sector": self.get_sector(),
            "maleta": bool(self.get_maleta()),
        })
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(reservas, f, ensure_ascii=False, indent=2)
