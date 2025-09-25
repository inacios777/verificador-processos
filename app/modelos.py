"""
modelos.py

📌 Função deste arquivo:
Definir todos os modelos de dados usados no sistema, com Pydantic.
Isso garante que a entrada (Estrutura Base), a transformação (Estrutura Mínima)
e a saída (Resposta) estejam padronizadas.

-------------------------------------------------------------------------------
Três grupos de modelos:

1. Estrutura Base:
   ➡ Formato cru dos processos judiciais, como vem do tribunal.
   ➡ Entrada inicial do sistema.
   ➡ Contém documentos (texto livre) e movimentos (eventos em linha do tempo).

2. Estrutura Mínima:
   ➡ Versão simplificada e normalizada para aplicar as regras da política (POL-1 até POL-8).
   ➡ Saída do pré-processador.
   ➡ Campos são fixos, com status "Sim/Não" ou valores já prontos para análise.

3. Resposta:
   ➡ Saída final estruturada que a API/LLM deve retornar.
   ➡ Define se o processo é "aprovado", "rejeitado" ou "incompleto".
   ➡ Inclui justificativa textual e citações das regras de política aplicadas.

-------------------------------------------------------------------------------

"""

from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict, field_validator


# -------------------------------------------------------------------
# ENUM para resultado (compatível com o case)
# -------------------------------------------------------------------
class ResultadoEnum(str, Enum):
    approved = "approved"
    rejected = "rejected"
    incomplete = "incomplete"


# -------------------------------------------------------------------
# Estrutura Base (entrada bruta)
# -------------------------------------------------------------------
class Documento(BaseModel):
    id: str
    data_hora_juntada: datetime = Field(alias="dataHoraJuntada")
    nome: str
    texto: str

    model_config = ConfigDict(populate_by_name=True)


class Movimento(BaseModel):
    data_hora: datetime = Field(alias="dataHora")
    descricao: str

    model_config = ConfigDict(populate_by_name=True)


class ProcessoBase(BaseModel):
    numero_processo: str = Field(alias="numeroProcesso")
    classe: str
    orgao_julgador: str = Field(alias="orgaoJulgador")
    ultima_distribuicao: datetime = Field(alias="ultimaDistribuicao")
    assunto: str
    valor_causa: Optional[float] = Field(default=None, alias="valorCausa")
    valor_condenacao: Optional[float] = Field(default=None, alias="valorCondenacao")
    segredo_justica: bool = Field(alias="segredoJustica")
    justica_gratuita: bool = Field(alias="justicaGratuita")
    sigla_tribunal: str = Field(alias="siglaTribunal")
    esfera: str
    documentos: List[Documento]
    movimentos: List[Movimento]
    honorarios: Optional[Dict[str, float]] = None

    model_config = ConfigDict(populate_by_name=True)


# -------------------------------------------------------------------
# Estrutura Mínima (normalizada)
# -------------------------------------------------------------------
class ProcessoMinimo(BaseModel):
    numero_processo: str = Field(alias="numeroProcesso")
    classe: str
    orgao_julgador: str = Field(alias="orgaoJulgador")
    ultima_distribuicao: datetime = Field(alias="ultimaDistribuicao")
    valor_causa: Optional[float] = Field(default=None, alias="valorCausa")
    assunto: str
    segredo_justica: bool = Field(alias="segredoJustica")
    justica_gratuita: bool = Field(alias="justicaGratuita")
    sigla_tribunal: str = Field(alias="siglaTribunal")
    esfera: str
    valor_condenacao: Optional[float] = Field(default=None, alias="valorCondenacao")
    documentos: Dict[str, Dict]
    honorarios: Optional[Dict[str, float]] = None

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("valor_condenacao")
    def check_valor_condenacao(cls, v):
        if v is not None and v < 0:
            raise ValueError("O valor da condenação não pode ser negativo.")
        return v


# -------------------------------------------------------------------
# Saída do verificador (decisão final) → JSON compatível com o case
# -------------------------------------------------------------------
class RespostaDecisao(BaseModel):
    resultado: ResultadoEnum
    justificativa: str
    citacoes: List[str]

    model_config = ConfigDict(extra="forbid", populate_by_name=True)
