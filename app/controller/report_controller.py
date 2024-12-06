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
FATOR_EMISSAO_COMBUSTIVEL = 2.39  # tCO₂/litro (Diesel)
FATOR_EMISSAO_RESIDUOS = 1.83  # kgCO₂/kg


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

def calculate_vehicle_fleet_emissions(fleet: dict, duration: int) -> dict:
    """
    Calcula as emissões de carbono para a frota de veículos.
    """
    # Consumo total de combustível
    consumo_total = (
        fleet["numero_veiculos"] * fleet["consumo_mensal_por_veiculo"] * duration
    )

    # Emissões por combustível
    emissoes_combustivel = consumo_total * FATOR_EMISSAO_COMBUSTIVEL

    # Retorna o resultado
    return {
        "fuel_consumption": consumo_total,
        "fuel_emissions": emissoes_combustivel
    }

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

def calculate_waste_emissions(waste: dict, duration: int) -> dict:
    """
    Calcula as emissões de carbono para os resíduos.
    """
    # Emissões por resíduos
    emissoes_residuos = (
        waste["quantidade_residuos_kg_por_mes"] * duration * FATOR_EMISSAO_RESIDUOS
    )

    return {
        "waste_emissions": emissoes_residuos
    }

def calculate_transport_materials_emissions(transport: dict, duration: int) -> dict:
    """
    Calcula as emissões de carbono para o transporte de materiais.
    """
    # Distância total percorrida
    distancia_total = (
        transport["distancia_media_km"] * transport["numero_viagens_mensal"] * duration
    )
    
    # Emissões por transporte
    emissoes_transporte = (
        distancia_total * transport["consumo_litros_por_km"] * FATOR_EMISSAO_COMBUSTIVEL
    )

    return {
        "total_distance": distancia_total,
        "transport_emissions": emissoes_transporte
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

        # Calcula emissões da frota de veículos
        vehicle_fleet_emissions = calculate_vehicle_fleet_emissions(
            report_dict["frota_veiculos"], duration
        )

        # Calcula emissões do transporte de materiais
        transport_materials_emissions = calculate_transport_materials_emissions(
            report_dict["transporte_materiais"], duration
        )

        # Calcula emissões de resíduos
        waste_emissions = calculate_waste_emissions(
            report_dict["residuos_obra"], duration
        )

        # Adiciona os cálculos ao relatório
        report_dict["transmissions"] = {
            "building_materials": building_materials_emissions,
            "vehicle_fleet": vehicle_fleet_emissions,
            "transport_of_materials": transport_materials_emissions,
            "waste": waste_emissions
        }

        # Insere no MongoDB
        result = collection.insert_one(report_dict)
        return {
            "message": "Report created successfully",
            "id": str(result.inserted_id),
            "transmissions": {
                "building_materials": building_materials_emissions,
                "vehicle_fleet": vehicle_fleet_emissions,
                "transport_of_materials": transport_materials_emissions,
                "waste": waste_emissions
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
