from enums import TipoUsuario, TipoEquipamento

class Usuario:
    def __init__(self, id: str, nome: str, tipo: TipoUsuario):
        self.id = id
        self.nome = nome
        self.tipo = tipo
        self.emprestimos = []

    def pode_pegar(self, equipamento):
        if self.tipo in [TipoUsuario.PROFESSOR, TipoUsuario.TECNICO]:
            return True
        if self.tipo == TipoUsuario.ALUNO_POS:
            return equipamento.tipo != TipoEquipamento.FERRAMENTA
        if self.tipo == TipoUsuario.ALUNO_GRADUACAO:
            return equipamento.tipo in [TipoEquipamento.COMPONENTE, TipoEquipamento.PLACA]
        return False
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'tipo': self.tipo.value,
            'emprestimos': self.emprestimos
        }
    
    @classmethod
    def from_dict(cls, data):
        usuario = cls(
            data['id'],
            data['nome'],
            TipoUsuario.from_str(data['tipo'])
        )
        usuario.emprestimos = data['emprestimos']
        return usuario