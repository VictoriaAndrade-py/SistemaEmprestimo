import datetime
from enums import TipoEquipamento

class Equipamento:
    def __init__(self, id: str, nome: str, tipo: TipoEquipamento):
        self.id = id
        self.nome = nome
        self.tipo = tipo
        self.disponivel = True
        self.historico = []

    def emprestar(self, usuario):
        if not self.disponivel:
            return False, "Indisponível"
            
        registro = {
            'usuario': usuario.nome,
            'data': datetime.datetime.now().isoformat()
        }
        self.historico.append(registro)
        self.disponivel = False
        return True, "Empréstimo realizado"

    def devolver(self):
        self.disponivel = True
        return True, "Devolução realizada"
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'tipo': self.tipo.value,
            'disponivel': self.disponivel,
            'historico': self.historico
        }
    
    @classmethod
    def from_dict(cls, data):
        equip = cls(
            data['id'],
            data['nome'],
            TipoEquipamento.from_str(data['tipo'])
        )
        equip.disponivel = data['disponivel']
        equip.historico = data['historico']
        return equip