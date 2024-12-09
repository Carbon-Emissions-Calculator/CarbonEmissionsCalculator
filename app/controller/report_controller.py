from app.model.report_model import Report
from app.model.database import db
from pymongo import ReturnDocument
from app.calculator.calculator import calculate_building_materials_emissions, calculate_waste_emissions, calculate_transport_materials_emissions, calculate_vehicle_fleet_emissions

# Referência à coleção no MongoDB
collection = db["reports"]

# Coleção para contadores
counters_collection = db["counters"]

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

def create_report(data: dict):
    """
    Cria um novo relatório no MongoDB.
    """
    try:
        # Gera o ID automaticamente
        data["id"] = get_next_sequence("report_id")
        newId = data["id"]

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

        total_emissions = building_materials_emissions["cement"] + building_materials_emissions["steel"] + vehicle_fleet_emissions["fuel_consumption"] + vehicle_fleet_emissions["fuel_emissions"] + transport_materials_emissions["total_distance"] + transport_materials_emissions["transport_emissions"] + waste_emissions["waste_emissions"]

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
            "id": str(newId),
            "transmissions": {
                "building_materials": building_materials_emissions,
                "vehicle_fleet": vehicle_fleet_emissions,
                "transport_of_materials": transport_materials_emissions,
                "waste": waste_emissions,
                "total": {"total_emissions": total_emissions}
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
                "uuid:": str(report["_id"]),
                "id": str(report["id"]),
                "name": report["informacoes_gerais"]["nome_da_obra"]
            }
            for report in reports
        ]
    except Exception as e:
        return {"error": str(e)}

def get_report_by_id(report_id: int):
    """
    Busca um relatório específico pelo ID no MongoDB e calcula as emissões.
    """
    try:
        # Busca o relatório no MongoDB
        inputData = collection.find_one({"id": int(report_id)})
        if not inputData:
            return {"error": "Report not found"}

        # Carrega os dados do relatório e calcula as emissões
        duration = inputData["informacoes_gerais"]["duracao_em_meses"]
        building_materials_emissions = calculate_building_materials_emissions(
            inputData["materiais_construcao"], duration
        )
        vehicle_fleet_emissions = calculate_vehicle_fleet_emissions(
            inputData["frota_veiculos"], duration
        )
        transport_materials_emissions = calculate_transport_materials_emissions(
            inputData["transporte_materiais"], duration
        )
        waste_emissions = calculate_waste_emissions(
            inputData["residuos_obra"], duration
        )

        total_emissions = building_materials_emissions["cement"] + building_materials_emissions["steel"] + vehicle_fleet_emissions["fuel_consumption"] + vehicle_fleet_emissions["fuel_emissions"] + transport_materials_emissions["total_distance"] + transport_materials_emissions["transport_emissions"] + waste_emissions["waste_emissions"]

        # Retorna os dados do relatório com os cálculos
        return {
            "id": str(inputData["id"]),
            "name": inputData["informacoes_gerais"]["nome_da_obra"],
            "transmissions": {
                "building_materials": building_materials_emissions,
                "vehicle_fleet": vehicle_fleet_emissions,
                "transport_of_materials": transport_materials_emissions,
                "waste": waste_emissions,
                "total": {"total_emissions": total_emissions}
            }
        }
    except Exception as e:
        return {"error": str(e)}


def delete_report_by_id(report_id: int):
    """
    Deleta um relatório específico pelo ID no MongoDB.
    """
    try:
        # Tenta encontrar e deletar o relatório
        result = collection.delete_one({"id": int(report_id)})
        if result.deleted_count > 0:
            return {"message": f"Report with ID {report_id} deleted successfully."}
        else:
            return {"error": f"No report found with ID {report_id}."}
    except Exception as e:
        return {"error": str(e)}
