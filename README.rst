RAPOSA
======

Lexicological framework for pipeline text processing


Description
------------

RAPOSA processes texts word by word and applies different filters in a conveyor-belt like fashion.

Each filter first adds its own tags to each word according to their specific purpose, and then may decide to discard the word altogether after evaluating the tags present.

The words that reach the end of this pipeline are output along with their tags and context information. The particular set of filters and their order of application is chosen by the user from the available pool in each run.

The intended use case for RAPOSA is lexicology analysis, being of special convenience for neology, lexicography and morphology, but its open-endedness and customization allow for many different kinds of purposes. For this reason, it also includes many other NLP/CompLing goodies.

RAPOSA is not tied to any specific language, though currently it may only contain filters for some languages due to obvious time development constraints. RAPOSA is specially proud to support minorized and minority languages.

Contributions are always warmly welcome and appreciated!


Use
---

As the software is under development, look at ``demo.py`` for examples until proper docs are in place.


Patronage
------

The initial version of this package has been developed under a research scholarship from the Deputación da Coruña for the year 2016.


License
-------

The software is released under a MIT License (see `LICENSE` file in the root folder for details), except for the following resources, which are derivative work:

- Module ``langs.gl.stemming`` is an adaptation of the code at http://bvg.udc.es/recursos_lingua/stemming.jsp, copyright 2006 Biblioteca Virtual Galega

- The data in ``langs/es/data/drae_2011.dat`` is taken from the lemmas for the Diccionario de la Real Academia Española as release at http://dirae.es/

- The data in ``langs/es/data/nombres_2016.dat`` and ``langs/es/data/apellidos_2016.dat`` is taken from official data from the Spanish Instituto Nacional de Estadística: http://www.ine.es/dyngs/INEbase/es/operacion.htm?c=Estadistica_C&cid=1254736177009&menu=resultados&idp=1254734710990

- The data in ``langs/gl/data/corga_1.7.dat`` is taken from the frequency list of the Corpus de Referencia do Galego Actual: http://corpus.cirp.es/corga/ As such, this modified lexicon is released under the terms of the Lesser General Public License For Linguistic Resources as the original. See ``LICENSE`` file in that folder for details.

- The data in ``langs/gl/data/xiada_2.6.dat`` is taken from the XIADA project by the Centro Ramón Piñeiro para a Investigación en Humanidades: http://corpus.cirp.es/xiada/ As such, this modified lexicon is released under the terms of the Lesser General Public License For Linguistic Resources as the original. See ``LICENSE`` file in that folder for details.

- The data in ``lans/gl/data/estraviz_09_2017.dat`` is taken from the sitemaps for the Dicionário Estraviz: http://estraviz.org/

- The data in ``langs/gl/data/toponimia_2013.dat`` is taken from official data from the Xunta de Galicia: http://abertos.xunta.gal/catalogo/territorio-vivienda-transporte/-/dataset/0159/microtoponimia-galicia
