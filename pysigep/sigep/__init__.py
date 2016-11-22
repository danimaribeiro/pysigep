# -*- coding: utf-8 -*-
# #############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) 2016 Michell Stuttgart
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
###############################################################################

from pysigep.webservices import WebserviceFrete
from pysigep.webservices.webservice_sigep import WebserviceSIGEP
from pysigep.campos import (
    CampoString,
    CampoCEP,
    CampoInteiro,
    CampoDecimal
)
from pysigep.base import RequestBaseSIGEPAuthentication
from pysigep.base import RequestBaseFrete


class BuscaCliente(RequestBaseSIGEPAuthentication):

    def __init__(self, id_contrato, id_cartao_postagem, usuario, senha):
        super(BuscaCliente, self).__init__(
            BuscaCliente, usuario, senha)

        self.id_contrato = CampoString(
            'idContrato', obrigatorio=True, valor=id_contrato, tamanho=10)
        self.id_cartao_postagem = CampoString(
            'idCartaoPostagem', valor=id_cartao_postagem,
            obrigatorio=True, tamanho=10)

    def get_data(self):
        xml = RequestBaseSIGEPAuthentication.HEADER
        xml += '<cli:buscaCliente>'
        xml += self.id_contrato.get_xml()
        xml += self.id_cartao_postagem.get_xml()
        xml += super(BuscaCliente, self).get_data()
        xml += '</cli:buscaCliente>'
        xml += RequestBaseSIGEPAuthentication.FOOTER
        return xml

    def execute(self):
        server = WebserviceSIGEP('HOMOLOGACAO')
        response = server.request(self)
        return response.Body.buscaClienteResponse["return"]


class CalcularPrecoPrazo(RequestBaseFrete):

    FORMATO_CAIXA_PACOTE = 1
    FORMATO_ROLO_PRISMA = 2
    FORMATO_ENVELOPE = 3

    def __init__(self, cod_administrativo, senha, nCdServico, sCepOrigem,
                 sCepDestino, nVlPeso,
                 nCdFormato, nVlComprimento, nVlAltura, nVlLargura,
                 nVlDiametro, sCdMaoPropria, nVlValorDeclarado,
                 sCdAvisoRecebimento):

        super(CalcularPrecoPrazo, self).__init__(CalcularPrecoPrazo)

        self.ncdempresa = CampoString('nCdEmpresa', valor=cod_administrativo)
        self.sdssenha = CampoString('sDsSenha', valor=senha)
        self.nCdServico = CampoString('nCdServico', valor=nCdServico,
                                      obrigatorio=True)
        self.sCepOrigem = CampoCEP('sCepOrigem', valor=sCepOrigem,
                                   obrigatorio=True)
        self.sCepDestino = CampoCEP('sCepDestino', valor=sCepDestino,
                                    obrigatorio=True)
        self.nVlPeso = CampoString('nVlPeso', valor=nVlPeso, obrigatorio=True)
        self.nCdFormato = CampoInteiro('nCdFormato', valor=nCdFormato,
                                       obrigatorio=True)
        self.nVlComprimento = CampoDecimal('nVlComprimento',
                                           valor=nVlComprimento,
                                           obrigatorio=True)
        self.nVlAltura = CampoDecimal('nVlAltura', valor=nVlAltura,
                                      obrigatorio=True)
        self.nVlLargura = CampoDecimal('nVlLargura', valor=nVlLargura,
                                       obrigatorio=True)
        self.nVlDiametro = CampoDecimal('nVlDiametro', valor=nVlDiametro,
                                        obrigatorio=True)
        self.sCdMaoPropria = CampoString('sCdMaoPropria', obrigatorio=True,
                                         valor='S' if sCdMaoPropria else 'N')
        self.nVlValorDeclarado = CampoDecimal('nVlValorDeclarado',
                                              valor=nVlValorDeclarado)
        self.sCdAvisoRecebimento = CampoString('sCdAvisoRecebimento',
                                               valor='S' if sCdAvisoRecebimento
                                               else 'N')

    def get_data(self):

        xml = RequestBaseFrete.HEADER
        xml += '<CalcPrecoPrazo xmlns=\"http://tempuri.org/\">'
        xml += self.ncdempresa.get_xml()
        xml += self.sdssenha.get_xml()
        xml += self.nCdServico.get_xml()
        xml += self.sCepOrigem.get_xml()
        xml += self.sCepDestino.get_xml()
        xml += self.nVlPeso.get_xml()
        xml += self.nCdFormato.get_xml()
        xml += self.nVlComprimento.get_xml()
        xml += self.nVlAltura.get_xml()
        xml += self.nVlLargura.get_xml()
        xml += self.nVlDiametro.get_xml()
        xml += self.sCdMaoPropria.get_xml()
        xml += self.nVlValorDeclarado.get_xml()
        xml += self.sCdAvisoRecebimento.get_xml()
        xml += '</CalcPrecoPrazo>'
        xml += RequestBaseFrete.FOOTER

        return xml

    def execute(self):
        server = WebserviceFrete()
        response = server.request(self)
        return response.Body.CalcPrecoPrazoResponse.CalcPrecoPrazoResult
