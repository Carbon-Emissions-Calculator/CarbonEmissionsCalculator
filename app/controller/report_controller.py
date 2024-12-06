from app.model.report_model import Report
from app.model.database import db
from pymongo import ReturnDocument

def calculate_emissions(data: dict, duration: int) -> dict:
    """
    Calcula as emissões de carbono com base nos diferentes fatores.

    Parâmetros:
        data (dict): Dados de entrada contendo informações necessárias para os cálculos.
        duration (int): Duração do projeto em meses.

    Retorno:
        dict: Emissões calculadas para cada categoria.
    """

    # Fatores de emissão
    FATOR_EMISSAO_CIMENTO = 0.93  # tCO₂/tonelada
    FATOR_EMISSAO_ACO = 1.83  # tCO₂/tonelada
    FATOR_EMISSAO_DIESEL = 2.68  # kgCO₂/litro
    FATOR_EMISSAO_ELETRICIDADE = 0.4  # kgCO₂/kWh
    FATOR_EMISSAO_RESIDUOS = 1.83  # kgCO₂/kg

    # Materiais de Construção
    cimento_emissoes = (
        data.get("cimento_toneladas_por_mes", 0) * duration * FATOR_EMISSAO_CIMENTO
    )
    aco_emissoes = (
        data.get("aco_toneladas_por_mes", 0) * duration * FATOR_EMISSAO_ACO
    )

    # Consumo de Energia
    diesel_emissoes = (
        data.get("consumo_mensal_diesel", 0) * duration * FATOR_EMISSAO_DIESEL
    )
    eletricidade_emissoes = (
        data.get("consumo_mensal_kwh", 0) * duration * FATOR_EMISSAO_ELETRICIDADE
    )

    # Transporte de Materiais
    distancia_total = (
        data.get("distancia_media_km", 0)
        * data.get("numero_viagens_mensal", 0)
        * duration
    )
    transporte_emissoes = (
        distancia_total
        * data.get("consumo_litros_por_km", 0)
        * FATOR_EMISSAO_DIESEL
    )

    # Resíduos
    residuos_emissoes = (
        data.get("quantidade_residuos_kg_por_mes", 0)
        * duration
        * FATOR_EMISSAO_RESIDUOS
    )

    # Frota de Veículos
    consumo_total_combustivel = (
        data.get("numero_veiculos", 0)
        * data.get("consumo_mensal_por_veiculo", 0)
        * duration
    )
    veiculos_emissoes = consumo_total_combustivel * FATOR_EMISSAO_DIESEL

    # Resultado
    return {
        "materials": {
            "cement": cimento_emissoes,
            "steel": aco_emissoes,
        },
        "energy": {
            "diesel": diesel_emissoes,
            "electricity": eletricidade_emissoes,
        },
        "transport": {
            "distance_total_km": distancia_total,
            "emissions": transporte_emissoes,
        },
        "waste": residuos_emissoes,
        "vehicles": veiculos_emissoes,
    }

def get_next_sequence(sequence_name: str) -> int:
    """
    Gera o próximo número da sequência para o ID do relatório.
    """
    counters_collection = db["counters"]
    counter = counters_collection.find_one_and_update(
        {"_id": sequence_name},  # Nome da sequência
        {"$inc": {"seq": 1}},  # Incrementa o valor da sequência
        upsert=True,  # Cria o documento se não existir
        return_document=ReturnDocument.AFTER  # Retorna o documento atualizado
    )
    return counter["seq"]

def create_report(data: dict):
    """
    Cria um novo relatório no MongoDB.
    """
    try:
        # Referência à coleção no MongoDB
        collection = db["reports"]

        # Gera o ID automaticamente
        data["id"] = get_next_sequence("report_id")

        # Valida e cria o relatório
        inputReport = Report(**data)
        report_dict = inputReport.dict()

        # Extrai a duração do projeto
        duration = data["informacoes_gerais"]["duracao_em_meses"]

        # Calcula as emissões de carbono com base nos dados fornecidos
        emissions = calculate_emissions(report_dict, duration)

        # Adiciona os cálculos ao relatório
        report_dict["transmissions"] = emissions

        # Insere no MongoDB
        result = collection.insert_one(report_dict)
        return {
            "message": "Report created successfully",
            "id": str(result.inserted_id),
            "transmissions": emissions
        }
    except Exception as e:
        return {"error": str(e)}

def get_all_reports():
    """
    Busca todos os relatórios no MongoDB.
    """
    try:
        collection = db["reports"]
        reports = list(collection.find())
        return [
            {
                "id": str(report["_id"]),
                "name": report["informacoes_gerais"]["nome_da_obra"]
            }
            for report in reports
        ]
    except Exception as e:
        return {"error": str(e)}

def get_report_by_id(report_id: str):
    """
    Busca um relatório específico pelo ID no MongoDB.
    """
    try:
        collection = db["reports"]
        inputData = collection.find_one({"_id": db.ObjectId(report_id)})
        if inputData:
            return {
                "id": str(inputData["_id"]),
                "name": inputData["informacoes_gerais"]["nome_da_obra"],
                "transmissions": inputData.get("transmissions", {})
            }
        return {"error": "Report not found"}
    except Exception as e:
        return {"error": str(e)}

# Exemplo de uso:
data = {
    "informacoes_gerais": {"duracao_em_meses": 12, "nome_da_obra": "Projeto A"},
    "cimento_toneladas_por_mes": 100,
    "aco_toneladas_por_mes": 50,
    "consumo_mensal_diesel": 200,
    "consumo_mensal_kwh": 5000,
    "distancia_media_km": 50,
    "numero_viagens_mensal": 20,
    "consumo_litros_por_km": 0.2,
    "quantidade_residuos_kg_por_mes": 1000,
    "numero_veiculos": 10,
    "consumo_mensal_por_veiculo": 150,
}

report = create_report(data)
print(report)
