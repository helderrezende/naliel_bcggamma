## Intro

20 de Outubro e 09 de Novembro | BCG São Paulo

Em uma parceria inédita entre BCG GAMMA, Abrale e Observatório de Oncologia, você terá a oportunidade de entender as necessidades do setor, trazer ideias sobre como endereçar problemas e, por fim, apresentar sua solução para a liderança das três organizações.


https://www.bcg.com/pt-br/careers/events/gamma-challenge/overview.aspx


## Installation

### Clone

```shell
$ git clone https://github.com/helderrezende/naliel_bcggamma.git
```
### Abrale data

Os dados da abrale devem estar dentro da pasta data/

### Download External data

```shell
$ cd naliel/
$ cd data/
$ gdown https://drive.google.com/uc?id=1uAcH2CPEgYVQyWLL5IX9GpLrfkmGeVQM
$ unzip external_data.zip
```


### Setup

MacOS:

```shell
$ conda create --name <env> python=3 pip
$ conda activate <env>
$ pip install -r requirements.txt
```

Windows:


```shell
$ conda create --name <env> python=3 pip
$ conda activate <env>
$ conda install -c conda-forge implicit
$ pip install -r requirements.txt
```

## Documentation

* Features - **Preprocessamento-SIA.ipynb**

* Modelo - **Modelo-Linfoma.ipynb**

      
## External data

* CEP - **tbl_cep_201908_n_log.csv** - (base paga):
  * Latitude
  * Longitude

* Municípios - **municipios.csv** (https://github.com/kelvins/Municipios-Brasileiros):
  * Latitude
  * Longitude
  
* Município Dados Economicos - **atlas2013_dadosbrutos_pt.csv** (http://www.atlasbrasil.org.br/2013/)
  
* Dados de Cnes - **cnesnone.csv** - (http://dados.gov.br/dataset/cnes)
   * Latitude
   * Longitude

* Investimento em Saúde - **orcamento.csv**(http://siops-asp.datasus.gov.br/CGI/deftohtm.exe?SIOPS/serhist/municipio/mIndicadores.def)

* Review hospital (Google Maps) - **reviews.csv** - feito manualmente


## Team - Naliel

* Helder Rezende (https://github.com/helderrezende)
* Natan Andrade (https://github.com/natandrade)
* Livia Parente (https://github.com/lvparente)


## Licença
Begin license text.

Copyright © 2019, naliel. Released under the MIT license.
      
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

End license text.
