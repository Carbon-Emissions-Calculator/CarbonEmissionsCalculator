from mongoengine import (
    Document, EmbeddedDocument, StringField, IntField, FloatField, BooleanField, ListField, DictField, EmbeddedDocumentField
)
from mongoengine import connect
from mongoengine.queryset import QuerySet

# Conectar ao MongoDB
connect(db="fastapi_db", host="localhost", port=27017)


# Modelo para ID autoincrementável
class Counter(Document):
    collection_name = StringField(required=True, unique=True)
    seq = IntField(default=0)


def get_next_sequence(collection_name):
    counter = Counter.objects(collection_name=collection_name).modify(
        upsert=True,
        new=True,
        inc__seq=1
    )
    return counter.seq


# Subdocumentos
class InformacoesGerais(EmbeddedDocument):
    nome_da_obra = StringField(required=True)
    localizacao = StringField(required=True)
    area_total_obra = IntField(required=True)
    duracao_em_meses = IntField(required=True)
    numero_trabalhadores = IntField(required=True)


class ConsumoEnergia(EmbeddedDocument):
    fonte_principal = StringField(required=True)
    consumo_mensal_kwh = IntField(default=0)
    consumo_mensal_diesel = IntField(default=0)
    outras_fontes = ListField(StringField(), default=[])


class TransporteMateriais(EmbeddedDocument):
    distancia_media_km = FloatField(required=True)
    numero_viagens_mensal = IntField(required=True)
    tipo_combustivel = StringField(required=True)
    consumo_litros_por_km = FloatField(required=True)


class ResiduosObra(EmbeddedDocument):
    quantidade_residuos_kg_por_mes = IntField(required=True)
    destinacao = StringField(required=True)
    percentual_reciclado = FloatField(required=True)


class MateriaisConstrucao(EmbeddedDocument):
    cimento_toneladas_por_mes = IntField(required=True)
    aco_toneladas_por_mes = IntField(required=True)
    madeira_m3_por_mes = FloatField(required=True)
    outros_materiais = DictField(default={})


class FrotaVeiculos(EmbeddedDocument):
    numero_veiculos = IntField(required=True)
    tipo_veiculos = ListField(StringField(), required=True)
    combustivel_veiculos = StringField(required=True)
    consumo_mensal_por_veiculo = IntField(required=True)


class DadosComplementares(EmbeddedDocument):
    compensacao_carbono = BooleanField(required=True)
    praticas_sustentaveis = StringField(required=True)


# Modelo Principal
class Report(Document):
    id = IntField(primary_key=True)
    informacoes_gerais = EmbeddedDocumentField(InformacoesGerais, required=True)
    consumo_energia = EmbeddedDocumentField(ConsumoEnergia, required=True)
    transporte_materiais = EmbeddedDocumentField(TransporteMateriais, required=True)
    residuos_obra = EmbeddedDocumentField(ResiduosObra, required=True)
    materiais_construcao = EmbeddedDocumentField(MateriaisConstrucao, required=True)
    frota_veiculos = EmbeddedDocumentField(FrotaVeiculos, required=True)
    dados_complementares = EmbeddedDocumentField(DadosComplementares, required=True)

    def save(self, *args, **kwargs):
        if not self.id:  # Gera o ID autoincrementável
            self.id = get_next_sequence("obra")
        super(Report, self).save(*args, **kwargs)
