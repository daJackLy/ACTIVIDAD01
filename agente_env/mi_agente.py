from entorno import Agente


class MiAgente(Agente):

    def __init__(self):
        super().__init__(nombre="Agente Utilidad")
        self.visitadas = set()
        self.historial = []
        self.retroceso = []

    def al_iniciar(self):
        """Se llama una vez al iniciar la simulación. Opcional."""
        self.visitadas = set()
        self.historial = []
        self.retroceso = []

    def decidir(self, percepcion):

        pos = percepcion['posicion']
        self.visitadas.add(pos)

        contraria = {
            'arriba': 'abajo', 'abajo': 'arriba',
            'izquierda': 'derecha', 'derecha': 'izquierda',
        }

        delta = {
            'arriba': (-1, 0), 'abajo': (1, 0),
            'izquierda': (0, -1), 'derecha': (0, 1),
        }

        for direccion in self.ACCIONES:
            if percepcion[direccion] == 'meta':
                return direccion

        if self.retroceso:
            return self.retroceso.pop(0)

        vert, horiz = percepcion['direccion_meta']

        preferencia = []
        if vert  != 'ninguna': preferencia.append(vert)
        if horiz != 'ninguna': preferencia.append(horiz)
        for a in self.ACCIONES:
            if a not in preferencia:
                preferencia.append(a)

        for direccion in preferencia:
            if percepcion[direccion] != 'libre':
                continue
            dr, dc = delta[direccion]
            vecino = (pos[0] + dr, pos[1] + dc)
            if vecino not in self.visitadas:
                self.historial.append(direccion)
                return direccion

        if self.historial:
            self.retroceso = [contraria[a] for a in reversed(self.historial)]
            self.historial = []
            return self.retroceso.pop(0)

        return 'abajo'