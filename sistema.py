import json
import os
from usuario import Usuario
from equipamento import Equipamento
from enums import TipoEquipamento  # Importação adicionada
from enums import TipoUsuario

class Sistema:
    ARQUIVO_DADOS = "dados_sistema.json"
    
    def __init__(self):
        self.usuarios = {}
        self.equipamentos = {}
        self.carregar_dados()
    
    def carregar_dados(self):
        if os.path.exists(self.ARQUIVO_DADOS):
            try:
                with open(self.ARQUIVO_DADOS, 'r') as f:
                    dados = json.load(f)
                    
                    # Carregar usuários
                    for usuario_data in dados.get('usuarios', []):
                        usuario = Usuario.from_dict(usuario_data)
                        self.usuarios[usuario.id] = usuario
                    
                    # Carregar equipamentos
                    for equip_data in dados.get('equipamentos', []):
                        equip = Equipamento.from_dict(equip_data)
                        self.equipamentos[equip.id] = equip
                        
                print("Dados carregados com sucesso!")
            except Exception as e:
                print(f"Erro ao carregar dados: {e}")
    
    def salvar_dados(self):
        dados = {
            'usuarios': [u.to_dict() for u in self.usuarios.values()],
            'equipamentos': [e.to_dict() for e in self.equipamentos.values()]
        }
        
        try:
            with open(self.ARQUIVO_DADOS, 'w') as f:
                json.dump(dados, f, indent=2)
            print("Dados salvos com sucesso!")
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
    
    def cadastrar_usuario(self):
        print("\n--- CADASTRAR USUÁRIO ---")
        id = input("ID do usuário: ")
        if id in self.usuarios:
            print("ID já existe!")
            return
            
        nome = input("Nome: ")
        print("Tipos: 1.Professor 2.Aluno Graduação 3.Aluno Pós 4.Técnico")
        tipo_op = input("Tipo: ")
        
        tipo_map = {
            "1": TipoUsuario.PROFESSOR,
            "2": TipoUsuario.ALUNO_GRADUACAO,
            "3": TipoUsuario.ALUNO_POS,
            "4": TipoUsuario.TECNICO
        }
        
        if tipo_op not in tipo_map:
            print("Tipo inválido!")
            return
            
        usuario = Usuario(id, nome, tipo_map[tipo_op])
        self.usuarios[id] = usuario
        self.salvar_dados()
        print(f"Usuário {nome} cadastrado!")

    def cadastrar_equipamento(self):
        print("\n--- CADASTRAR EQUIPAMENTO ---")
        id = input("ID do equipamento: ")
        if id in self.equipamentos:
            print("ID já existe!")
            return
            
        nome = input("Nome: ")
        print("Tipos: 1.Medição 2.Componente 3.Placa 4.Ferramenta 5.Outro")
        tipo_op = input("Tipo: ")
        
        tipo_map = {
            "1": TipoEquipamento.MEDICAO,
            "2": TipoEquipamento.COMPONENTE,
            "3": TipoEquipamento.PLACA,
            "4": TipoEquipamento.FERRAMENTA,
            "5": TipoEquipamento.OUTRO
        }
        
        if tipo_op not in tipo_map:
            print("Tipo inválido!")
            return
            
        equip = Equipamento(id, nome, tipo_map[tipo_op])
        self.equipamentos[id] = equip
        self.salvar_dados()
        print(f"Equipamento {nome} cadastrado!")

    def emprestar(self):
        print("\n--- REALIZAR EMPRÉSTIMO ---")
        user_id = input("ID do usuário: ")
        equip_id = input("ID do equipamento: ")
        
        usuario = self.usuarios.get(user_id)
        equipamento = self.equipamentos.get(equip_id)
        
        if not usuario:
            print("Usuário não encontrado!")
            return
            
        if not equipamento:
            print("Equipamento não encontrado!")
            return
            
        if not usuario.pode_pegar(equipamento):
            print("Usuário não tem permissão para este equipamento!")
            return
            
        success, msg = equipamento.emprestar(usuario)
        if success:
            usuario.emprestimos.append(equip_id)
            self.salvar_dados()
            print("Empréstimo realizado com sucesso!")
        else:
            print(f"Erro: {msg}")

    def devolver(self):
        print("\n--- REALIZAR DEVOLUÇÃO ---")
        equip_id = input("ID do equipamento: ")
        equipamento = self.equipamentos.get(equip_id)
        
        if not equipamento:
            print("Equipamento não encontrado!")
            return
            
        success, msg = equipamento.devolver()
        if success:
            # Encontra o usuário que tinha o equipamento
            for usuario in self.usuarios.values():
                if equip_id in usuario.emprestimos:
                    usuario.emprestimos.remove(equip_id)
            self.salvar_dados()
            print("Devolução realizada com sucesso!")
        else:
            print(f"Erro: {msg}")

    def listar(self):
        print("\n=== LISTAGEM COMPLETA ===")
        
        print("\n--- USUÁRIOS ({}) ---".format(len(self.usuarios)))
        for usuario in self.usuarios.values():
            print(f"[{usuario.id}] {usuario.nome} ({usuario.tipo.value})")
            if usuario.emprestimos:
                print(f"  Equipamentos emprestados: {', '.join(usuario.emprestimos)}")
        
        print("\n--- EQUIPAMENTOS ({}) ---".format(len(self.equipamentos)))
        for equip in self.equipamentos.values():
            status = "Disponível" if equip.disponivel else "Emprestado"
            print(f"[{equip.id}] {equip.nome} - {equip.tipo.value} ({status})")

    def menu(self):
        while True:
            print("\n" + "="*40)
            print("=== SISTEMA DE EMPRÉSTIMOS - LAB ELETRÔNICA ===")
            print("="*40)
            print("1. Cadastrar usuário")
            print("2. Cadastrar equipamento")
            print("3. Realizar empréstimo")
            print("4. Realizar devolução")
            print("5. Listar todos os cadastros")
            print("6. Sair")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "1":
                self.cadastrar_usuario()
            elif opcao == "2":
                self.cadastrar_equipamento()
            elif opcao == "3":
                self.emprestar()
            elif opcao == "4":
                self.devolver()
            elif opcao == "5":
                self.listar()
            elif opcao == "6":
                self.salvar_dados()
                print("\nObrigado por usar o sistema! Dados salvos.")
                break
            else:
                print("Opção inválida. Tente novamente.")