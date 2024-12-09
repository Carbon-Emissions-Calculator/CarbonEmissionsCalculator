# Fatores de emissão
FATOR_EMISSAO_CIMENTO = 0.93  # tCO₂/tonelada
FATOR_EMISSAO_ACO = 1.83  # tCO₂/tonelada
FATOR_EMISSAO_COMBUSTIVEL = 2.39  # tCO₂/litro (Diesel)
FATOR_EMISSAO_RESIDUOS = 1.83  # kgCO₂/kg

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