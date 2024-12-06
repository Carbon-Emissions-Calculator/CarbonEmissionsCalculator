from pydantic import BaseModel
from typing import List, Dict, Optional

# Subdocumentos como Pydantic Models
class InformacoesGerais(BaseModel):
    nome_da_obra: str
    localizacao: str
    area_total_obra: int
    duracao_em_meses: int
    numero_trabalhadores: int


class ConsumoEnergia(BaseModel):
    fonte_principal: str
    consumo_mensal_kwh: Optional[int] = 0
    consumo_mensal_diesel: Optional[int] = 0
    outras_fontes: Optional[List[str]] = []


class TransporteMateriais(BaseModel):
    distancia_media_km: float
    numero_viagens_mensal: int
    tipo_combustivel: str
    consumo_litros_por_km: float


class ResiduosObra(BaseModel):
    quantidade_residuos_kg_por_mes: int
    destinacao: str
    percentual_reciclado: float


class MateriaisConstrucao(BaseModel):
    cimento_toneladas_por_mes: int
    aco_toneladas_por_mes: int
    madeira_m3_por_mes: float
    outros_materiais: Optional[Dict] = {}


class FrotaVeiculos(BaseModel):
    numero_veiculos: int
    tipo_veiculos: List[str]
    combustivel_veiculos: str
    consumo_mensal_por_veiculo: int


class DadosComplementares(BaseModel):
    compensacao_carbono: bool
    praticas_sustentaveis: str


# Modelo Principal
class Report(BaseModel):
    id: Optional[int]  # ID será atribuído no controlador
    informacoes_gerais: InformacoesGerais
    consumo_energia: ConsumoEnergia
    transporte_materiais: TransporteMateriais
    residuos_obra: ResiduosObra
    materiais_construcao: MateriaisConstrucao
    frota_veiculos: FrotaVeiculos
    dados_complementares: DadosComplementares