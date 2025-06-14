from enum import Enum

class TipoUsuario(Enum):
    PROFESSOR = "Professor"
    ALUNO_GRADUACAO = "Aluno de Graduação"
    ALUNO_POS = "Aluno de Pós-Graduação"
    TECNICO = "Técnico"

    @classmethod
    def from_str(cls, s):
        for tipo in cls:
            if tipo.value == s:
                return tipo
        return None

class TipoEquipamento(Enum):
    MEDICAO = "Equipamento de Medição"
    COMPONENTE = "Componente Eletrônico"
    PLACA = "Placa de Desenvolvimento"
    FERRAMENTA = "Ferramenta"
    OUTRO = "Outro"

    @classmethod
    def from_str(cls, s):
        for tipo in cls:
            if tipo.value == s:
                return tipo
        return None