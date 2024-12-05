# Mock database (em memória)
mock_db = []
counter = 0  # Simula o autoincremento do ID

class MockReport:
    def __init__(self, **kwargs):
        global counter
        counter += 1
        self.id = counter  # ID autoincrementável
        
        # Mapeia os dados do JSON para os atributos do objeto
        self.informacoes_gerais = kwargs.get("informacoes_gerais", {})
        self.consumo_energia = kwargs.get("consumo_energia", {})
        self.transporte_materiais = kwargs.get("transporte_materiais", {})
        self.residuos_obra = kwargs.get("residuos_obra", {})
        self.materiais_construcao = kwargs.get("materiais_construcao", {})
        self.frota_veiculos = kwargs.get("frota_veiculos", {})
        self.dados_complementares = kwargs.get("dados_complementares", {})

    def save(self):
        """Simula a inserção no banco de dados."""
        mock_db.append(self)

    @classmethod
    def objects(cls):
        """Retorna todos os objetos no banco mockado."""
        return mock_db

    @classmethod
    def get(cls, report_id):
        """Busca um objeto pelo ID."""
        for obra in mock_db:
            if obra.id == report_id:
                return obra
        return None

    @classmethod
    def delete(cls, report_id):
        """Remove um objeto do banco mockado."""
        global mock_db
        mock_db = [obra for obra in mock_db if obra.id != obra_id]
