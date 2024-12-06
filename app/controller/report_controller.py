from app.model.report_model import Report
from app.model.database import db
from pymongo import ReturnDocument

# Referência à coleção no MongoDB
collection = db["reports"]

# Coleção para contadores
counters_collection = db["counters"]

# Fatores de emissão
FATOR_EMISSAO_CIMENTO = 0.93  # tCO₂/tonelada
FATOR_EMISSAO_ACO = 1.83  # tCO₂/tonelada

def get_next_sequence(sequence_name: str) -> int:
    """
    Gera o próximo número da sequência para o ID do relatório.
    """
    counter = counters_collection.find_one_and_update(
        {"_id": sequence_name},  # Nome da sequência
        {"$inc": {"seq": 1}},  # Incrementa o valor da sequência
        upsert=True,  # Cria o documento se não existir
        return_document=ReturnDocument.AFTER  # Retorna o documento atualizado
    )
    return counter["seq"]

def calculate_building_materials_emissions(materials: dict, duration: int) -> dict:
    """
    Calcula as emissões de carbono para materiais de construção.
    """
    # Cálculo para cimento
    cimento_emissoes = (
        materials["cimento_toneladas_por_mes"] * duration * FATOR_EMISSAO_CIMENTO
    )
    
    # Cálculo para aço
    aco_emissoes = (
        materials["aco_toneladas_por_mes"] * duration * FATOR_EMISSAO_ACO
    )
    
    # Retorna o resultado
    return {
        "cement": cimento_emissoes,
        "steel": aco_emissoes
    }

def create_report(data: dict):
    """
    Cria um novo relatório no MongoDB.
    """
    try:
        # Gera o ID automaticamente
        data["id"] = get_next_sequence("report_id")

        # Valida e cria o relatório
        inputReport = Report(**data)
        report_dict = inputReport.dict()

        # Calcula emissões de materiais de construção
        duration = data["informacoes_gerais"]["duracao_em_meses"]
        building_materials_emissions = calculate_building_materials_emissions(
            report_dict["materiais_construcao"], duration
        )
        
        # Adiciona os cálculos ao relatório
        report_dict["transmissions"] = {
            "building_materials": building_materials_emissions
        }

        # Insere no MongoDB
        result = collection.insert_one(report_dict)
        return {
            "message": "Report created successfully",
            "id": str(result.inserted_id),
            "transmissions": {
                "building_materials": building_materials_emissions
            }
        }
    except Exception as e:
        return {"error": str(e)}

def get_all_reports():
    """
    Busca todos os relatórios no MongoDB.
    """
    try:
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
        inputData = collection.find_one({"_id": db.ObjectId(report_id)})
        if inputData:
            return {
                "id": str(inputData["_id"]),
                "name": inputData["informacoes_gerais"]["nome_da_obra"],
                "transmissions": {
                    "energy_consumption": {
                        "diesel": 1000,
                        "others": None
                    },
                    "transport_of_materials": {
                        "total_distance": 1000,
                        "transmissions_per_transport": 1000
                    },
                    "wastes": {
                        "emissions_per_waste": 1
                    },
                    "building_materials": {
                        "cement": 10,
                        "steel": 10,
                        "others": None
                    },
                    "vehicles_fleet": {
                        "fuel_consumption": 10,
                        "emissions_per_fuel": 10
                    }
                }
            }
        return {"error": "Report not found"}
    except Exception as e:
        return {"error": str(e)}
