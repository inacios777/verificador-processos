"""

📌 Função deste arquivo:

Definir todas as estruturas de dados que o sistema manipula, utilizando Pydantic para validação e tipagem.
Organiza desde a entrada bruta dos processos, até a versão normalizada e a resposta final estruturada.

------------------------------------------------------------------------------------------------------------------------
Três blocos principais:

Estrutura Base (entrada bruta):
➡ Representa os processos judiciais exatamente como recebidos do tribunal.
➡ Inclui documentos e movimentos originais, além de dados como valores, classe e órgão julgador.
➡ Serve como ponto de partida para o pré-processamento.

Estrutura Mínima (normalizada):
➡ Versão simplificada e organizada para análise de regras.
➡ Converte documentos em dicionários, padroniza campos e aplica validações (ex.: impedir valores negativos em condenação).
➡ Saída do pré-processador, pronta para uso pelas políticas de decisão.

Saída do Verificador (decisão final):
➡ Modelo de resposta que a API/LLM deve retornar.
➡ Contém o resultado (approved / rejected / incomplete), a justificativa textual e citações das regras aplicadas.
➡ Estrutura compatível com o case final de decisão.

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
