# from app.model.report_model import User
from app.model.report_mock import MockReport as Report
from app.calculator.calculator import operation1

def create_report(data: dict):
    try:
        inputReport = Report(**data)
        inputReport.save()
        return {
                "message": "Report created successfully",
                "id": str(inputReport.id),
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
    except Exception as e:
        return {"error": str(e)}

def get_all_reports():
    inputsData = Report.objects()
    return [{"id": str(input.id),
             "name": input.informacoes_gerais["nome_da_obra"]} for input in inputsData]

def get_report_by_id(report_id: str):
    try:
        inputData = Report.get(report_id=int(report_id))
        if inputData:
            return {
                    "id": str(inputData.id),
                    "name": inputData.informacoes_gerais["nome_da_obra"],
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

# def update_user(user_id: str, data: dict):
#     try:
#         user = Data.objects(id=user_id).first()
#         if user:
#             user.update(**data)
#             return {"message": "User updated successfully"}
#         return {"error": "User not found"}
#     except Exception as e:
#         return {"error": str(e)}

# def delete_user(user_id: str):
#     try:
#         user = Data.objects(id=user_id).first()
#         if user:
#             user.delete()
#             return {"message": "User deleted successfully"}
#         return {"error": "User not found"}
#     except Exception as e:
#         return {"error": str(e)}



#### Formato de input
# {
#     "informacoes_gerais": {
#         "nome_da_obra": "Ponte BH Norte",
#         "localizacao": "Belo Horizonte, MG",
#         "area_total_obra": 5000,
#         "duracao_em_meses": 18,
#         "numero_trabalhadores": 150
#     },
#     "consumo_energia": {
#         "fonte_principal": "Geradores a diesel",
#         "consumo_mensal_kwh": 0,
#         "consumo_mensal_diesel": 10000,
#         "outras_fontes": []
#     },
#     "transporte_materiais": {
#         "distancia_media_km": 50,
#         "numero_viagens_mensal": 30,
#         "tipo_combustivel": "Diesel",
#         "consumo_litros_por_km": 0.35
#     },
#     "residuos_obra": {
#         "quantidade_residuos_kg_por_mes": 10000,
#         "destinacao": "Reciclagem e aterro sanitário",
#         "percentual_reciclado": 60
#     },
#     "materiais_construcao": {
#         "cimento_toneladas_por_mes": 150,
#         "aco_toneladas_por_mes": 50,
#         "madeira_m3_por_mes": 10,
#         "outros_materiais": {
#             "asfalto": 500
#         }
#     },
#     "frota_veiculos": {
#         "numero_veiculos": 10,
#         "tipo_veiculos": ["Caminhões", "Guindastes"],
#         "combustivel_veiculos": "Diesel",
#         "consumo_mensal_por_veiculo": 1500
#     },
#     "dados_complementares": {
#         "compensacao_carbono": false,
#         "praticas_sustentaveis": "Reuso de água da chuva"
#     }
# }