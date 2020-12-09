from ...core.stemming.rule import Rule

class GLSimpleStemmer():

    # Simple Stemmer for Galician
    # adapted from:
    # http://bvg.udc.es/recursos_lingua/stemming.jsp
    # this implementation uses Rules, though
    # but the algorithm and rules are the same

    def __init__(self):
          self.suffixes = []
          self.s = ""
          self.m = str.maketrans('áéíóúêô', 'aeioueo')


    def _try_rule_block(self, rules, add=True):
        for rule in rules:
            success, m, result = rule.try_regress(self.s)
            if success:
                if add: # avoid adding ortographic stuff
                    self.suffixes.append(m)
                # many may come back, take just the first
                self.s = list(result)[0]
                return True
        return False


    def _remove_accents(self):
        self.s = self.s.translate(self.m)


    def stem(self, unit):

        self.s = unit.lower()
        self.suffixes = []

        if self.s.endswith("s") and len(self.s) >= 3:
           self._try_rule_block(PLURALS)

        self._try_rule_block(UNIFICATION, add=False)
        self._try_rule_block(ADVERBS)

        changes = True
        while (changes):
           changes = self._try_rule_block(AUGMENTATIVES)

        changes = self._try_rule_block(NOUNS)
        if not changes:
            self._try_rule_block(VERBS)

        self._try_rule_block(THEMATIC)
        self._remove_accents()

        chain = [self.s] + list(reversed(self.suffixes))

        # loop on the first element
        # this is the only extra thing added from the original
        if (self.s != unit.lower()):
           new_chain = self.stem(self.s)
           chain = new_chain + chain[1:]

        return chain


## PLURALS

PLURALS = [
    Rule("ns", 1, "n", ["luns", "furatapóns", "furatapons"]),
    Rule("ós", 3, "ón", []),
    Rule("ões", 3, "ón", []),
    Rule("ães", 1, "ão", ["mães", "magalhães"]),
    Rule("ais", 2, "al", ["cais","tais", "mais", "pais", "ademais"]),
    Rule("áis", 2, "al", ["cáis","táis", "máis", "páis", "ademáis"]),
    Rule("éis", 2, "el", []),
    Rule("eis", 2, "el", []),
    Rule("óis", 2, "ol", ["escornabóis"]),
    Rule("ois", 2, "ol", ["escornabois"]),
    Rule("ís", 2, "il", ["país"]),
    Rule("is", 2, "il", ["Menfis", "pais", "Kinguís"]),
    Rule("les", 2, "l", ["ingles", "marselles", "montreales", "senegales", "manizales", "móstoles", "nápoles"]),
    Rule("res", 3, "r", ["petres", "henares", "cáceres", "baleares", "linares", "londres", "mieres", "miraflores", "mércores", "venres", "pires"]),
    Rule("ces", 2, "z", []),
    Rule("zes", 2, "z", []),
    Rule("ises", 3, "z", []),
    Rule("ás", 1, "al", ["más"]),
    Rule("ses", 2, "s", []),
    Rule("s", 2, "", ["barbadés", "barcelonés", "cantonés", "gabonés", "llanés", "medinés", "escocés", "escocês", "francês", "barcelonês", "cantonês", "macramés", "reves", "barcelones", "cantones", "gabones", "llanes", "magallanes", "medines", "escoces", "frances", "xoves", "martes", "aliás","pires","lápis","cais","mais", "mas","menos", "férias","pêsames","crúcis", "país", "cangas", "atenas", "asturias", "canarias", "filipinas", "honduras", "molucas", "caldas", "mascareñas", "micenas", "covarrubias", "psoas", "óculos", "nupcias", "xoves", "martes", "llanes"]),
]


## UNIFICATION

UNIFICATION = [
    Rule("íssimo", 5, "ísimo", []),
    Rule("íssima", 5, "ísima", []),
    Rule("aço", 4, "azo", []),
    Rule("aça", 4, "aza", []),
    Rule("uça", 4, "uza", []),
    Rule("lhar", 2, "llar", []),
    Rule("lher", 2, "ller", []),
    Rule("lhor", 2, "llor", []),
    Rule("lho", 1, "llo", []),
    Rule("nhar", 2, "ñar", []),
    Rule("nhor", 2, "ñor", []),
    Rule("nho", 1, "ño", []),
    Rule("nha", 1, "ña", []),
    Rule("ário", 3, "ario", []),
    Rule("ária", 3, "aria", []),
    Rule("able", 2, "ábel", []),
    Rule("ável", 2, "ábel", []),
    Rule("ible", 2, "íbel", []),
    Rule("ível", 2, "íbel", []),
    Rule("çom", 2, "ción", []),
    Rule("agem", 2, "axe", []),
    Rule("age", 2, "axe", []),
    Rule("ão", 3, "ón", []),
    Rule("ao", 1, "án", []),
    Rule("au", 1, "án", []),
    Rule("om", 3, "ón", []),
    Rule("m", 2, "n", []),
]


## ADVERBS

ADVERBS = [
    Rule("mente", 4, "", ["experimente", "vehemente", "sedimente"])
]


## AUGMENTATIVES

AUGMENTATIVES = [
    Rule("d(í|i)simo", 5, "", []),
    Rule("d(í|i)sima", 5, "", []),
    Rule("bil(í|i)simo", 3, "", []),
    Rule("bil(í|i)sima", 3, "", []),
    Rule("(í|i)simo", 3, "", []),
    Rule("(í|i)sima", 3, "", []),
    Rule("(é|e)simo", 3, "", []),
    Rule("(é|e)sima", 3, "", []),
    Rule("(é|e)rrimo", 4, "", []),
    Rule("(é|e)rrima", 4, "", []),
    Rule("ana", 2, "", ["argana", "banana", "choupana", "espadana", "faciana", "iguana", "lantana", "macana", "membrana", "mesana", "nirvana", "obsidiana", "palangana", "pavana", "persiana", "pestana", "porcelana", "pseudomembrana", "roldana", "sábana", "salangana", "saragana", "ventana"]),
    Rule("(á|a)n", 3, "", ["ademán", "bardán", "barregán", "corricán", "curricán", "faisán", "furacán", "fustán", "gabán", "gabián", "galán", "gañán", "lavacán", "mazán", "mourán", "rabadán", "serán", "serrán", "tabán", "titán", "tobogán", "verán", "volcán", "volován"]),
    Rule("azo", 4, "", ["abrazo", "espazo", "andazo", "bagazo", "balazo", "bandazo", "cachazo",  "carazo", "denazo", "engazo", "famazo", "lampreazo",  "pantocazo", "pedazo", "preñazo", "regazo", "ribazo", "sobrazo", "terrazo", "trompazo"]),
    Rule("aza", 3, "", ["alcarraza", "ameaza",  "baraza", "broucaza", "burgaza", "cabaza", "cachaza", "calaza", "carpaza", "carraza", "coiraza", "colmaza", "fogaza", "famaza", "labaza", "liñaza", "melaza", "mordaza",  "paraza", "pinaza", "rabaza", "rapaza", "trancaza"]),
    Rule("allo", 4, "", ["traballo"]),
    Rule("alla", 4, "", []),
    Rule("arra", 3, "", ["cigarra", "cinzarra"]),
    Rule("astro", 3, "", ["balastro", "bimbastro", "canastro", "retropilastro"]),
    Rule("astra", 3, "", ["banastra", "canastra", "contrapilastra", "piastra", "pilastra"]),
    Rule("(á|a)zio", 3, "", ["topázio"]),
    Rule("elo", 4, "", ["bacelo", "barrelo", "bicarelo", "biquelo", "boquelo", "botelo", "bouquelo", "cacarelo", "cachelo", "cadrelo", "campelo", "candelo", "cantelo", "carabelo", "carambelo", "caramelo", "cercelo", "cerebelo", "chocarelo", "coitelo", "conchelo", "corbelo", "cotobelo", "couselo", "destelo", "desvelo", "esfácelo", "fandelo", "fardelo", "farelo", "farnelo", "flabelo", "ganchelo", "garfelo", "involucelo", "mantelo", "montelo", "outerelo", "padicelo", "pesadelo", "pinguelo", "piquelo", "rampelo", "rastrelo", "restelo", "tornecelo", "trabelo", "restrelo", "portelo", "ourelo", "zarapelo"]),
    Rule("eta", 3, "", ["arqueta", "atleta", "avoceta", "baioneta", "baldeta", "banqueta", "barraganeta", "barreta", "borleta", "buceta",
     "caceta", "calceta", "caldeta", "cambeta", "canaleta", "caneta", "carreta", "cerceta", "chaparreta", "chapeta", "chareta", "chincheta", "colcheta", "cometa",
     "corbeta", "corveta", " cuneta", "desteta", " espeta", "espoleta", "estafeta", "esteta", "faceta", "falanxeta", "frasqueta", "gaceta", "gabeta", "galleta",
     "garabeta", "gaveta", "glorieta", "lagareta", "lambeta", "lanceta", "libreta", "maceta", "macheta", "maleta", "malleta", "mareta", "marreta", "meseta",
     "mofeta", "muleta", "peseta", "planeta", "raqueta", "regreta", "saqueta", "vendeta", "viñeta"]),
    Rule("ete", 3, "", ["alfinete", "ariete", "bacinete", "banquete", "barallete", "barrete", "billete", "binguelete", "birrete", "bonete", "bosquete", "bufete", "burlete", "cabalete", "cacahuete", "cavinete", "capacete", "carrete", "casarete", "casete", "chupete", "clarinete", "colchete", "colete", "capete", "curupete", "disquete", "estilete", "falsete", "ferrete", "filete", "gallardete", "gobelete", "inglete", "machete", "miquelete", "molete", "mosquete", "piquete", "ribete", "rodete", "rolete", "roquete", "sorvete", "vedete", "veleta", "vendete"]),
    Rule("ica", 3, "", ["andarica", "botánica", "botica", "dialéctica", "dinámica", " física", "formica", "gráfica", "marica", "túnica"]),
    Rule("ico", 3, "", ["conico", "acetifico", "acidifico"]),
    Rule("exo", 3, "", ["arpexo", "arquexo", "asexo", "axexo", "azulexo", "badexo", "bafexo", "bocexo", "bosquexo", "boubexo", "cacarexo", "carrexo", "cascarexo", "castrexo", "convexo", "cotexo", "desexo", "despexo", "forcexo", "gabexo", "gargarexo", "gorgolexo", "inconexo", "manexo", "merexo", "narnexo", "padexo", "patexo", "sopexo", "varexo"]),
    Rule("exa", 3, "", ["airexa", "bandexa", "carrexa", "envexa", "igrexa", "larexa", "patexa", "presexa", "sobexa"]),
    Rule("idão", 3, "", []),
    Rule("iño", 3, "o", ["camiño", "cariño", "comiño", "golfiño", "padriño", "sobriño", "viciño", "veciño"]),
    Rule("iña", 3, "a", ["camariña", "campiña", "entreliña", "espiña", "fariña", "moriña", "valiña"]),
    Rule("ito", 3, "", []),
    Rule("ita", 3, "", []),
    Rule("oide", 3, "", ["anaroide", "aneroide", "asteroide", "axoide", "cardioide", "celuloide", "coronoide", "discoide", "espermatozoide", "espiroide", "esquizoide", "esteroide", "glenoide", "linfoide", "hemorroide", "melaloide", "sacaroide", "tetraploide", "varioloide"]),
    Rule("ola", 3, "", ["aixola", "ampola", "argola", "arola", "arteríolo", "bandola", "bítola", "bractéola", "cachola", "carambola", "carapola", "carola", "carrandiola", "catrapola", "cebola", "centola", "champola", "chatola", "cirola", "cítola", "consola", "corola", "empola", "escarola", "esmola", "estola", "fitola", "florícola", "garañola", "gárgola", "garxola", "glicocola", "góndola", "mariola", "marola", "michola", "pirola", "rebola", "rupícola", "saxícola", "sémola", "tachola", "tómbola"]),
    Rule("olo", 3, "", ["arrolo", "babiolo", "cacharolo", "caixarolo", "carolo", "carramolo", "cascarolo", "cirolo", "codrolo", "correolo", "cotrolo", "desconsolo", "rebolo", "repolo", "subsolo", "tixolo", "tómbolo", "torolo", "trémolo", "vacúolo", "xermolo", "zócolo"]),
    Rule("ote", 3, "", ["aigote", "alcaiote", "barbarote",  "balote", "billote", "cachote", "camarote", "capote", "cebote",  "chichote", "citote", "cocorote", "escote", "gañote", "garrote", "gavote", "lamote", "lapote", "larapote", "lingote", "lítote", "magore", "marrote", "matalote", "pandote", "paparote", "rebote", "tagarote", "zarrote"]),
    Rule("ota", 3, "", ["asíntota", "caiota", "cambota", "chacota", "compota", "creosota", "curota", "derrota", "díspota", "gamota", "maniota", "pelota", "picota", "pillota", "pixota", "queirota", "remota"]),
    Rule("cho", 3, "", ["abrocho", "arrocho", "carocho", "falucho", "bombacho", "borracho", "mostacho"]),
    Rule("cha", 3, "", ["borracha", "carracha", "estacha", "garnacha", "limacha", "remolacha", "abrocha"]),
    Rule("uco", 4, "", ["caduco", "estuco", "fachuco", "malluco", "saluco", "trabuco"]),
    Rule("uzo", 3, "", ["carriñouzo", "fachuzo", "mañuzo", "mestruzo", "tapuzo"]),
    Rule("uza", 3, "", ["barruza", "chamuza", "chapuza", "charamuza", "conduza", "deduza", "desluza", "entreluza", "induza", "recoñeza", "reluza", "seduza", "traduza", "trasluza"]),
    Rule("uxa", 3, "", ["caramuxa", "carrabouxa", "cartuxa", "coruxa", "curuxa", "gaturuxa", "maruxa", "meruxa", "miruxa", "moruxa", "muruxa",  "papuxa", "rabuxa", "trouxa"]),
    Rule("uxo", 3, "", ["caramuxo", "carouxo", "carrabouxo", "curuxo", "debuxo", "ganduxo", "influxo",  "negouxo", "pertuxo", "refluxo"]),
    Rule("ello", 3, "", ["alborello", "artello", "botello", "cachafello",  "calello", "casarello", "cazabello", "cercello", "cocerello", "concello", "consello", "desparello", "escaravello", "espello", "fedello", "fervello", "gagafello", "gorrobello", "nortello", "pendello", "troupello", "trebello"]),
    Rule("ella", 3, "", ["alborella", "bertorella", "bocatella", "botella", "calella", "cercella", "gadella", "grosella", "lentella", "movella", "nocella", "noitevella", "parella", "pelella", "percebella", "segorella", "sabella"])
]


## NOUN ENDINGS

NOUNS = [
    Rule("dade", 3, "", ["acridade", "calidade"]),
    Rule("ificar", 2, "", []),
    Rule("eiro", 3, "", ["agoireiro", "bardalleiro", "braseiro", "barreiro", "canteiro", "capoeiro", "carneiro", "carteiro", "cinceiro", "faroleiro", "mareiro", "preguiceiro", "quinteiro", "raposeiro", "retranqueiro", "regueiro", "sineiro", "troleiro", "ventureiro"]),
    Rule("eira", 3, "", ["cabeleira", "canteira", "cocheira", "folleira", "milleira"]),
    Rule("ario", 3, "", ["armario", "calcario", "lionario", "salario"]),
    Rule("aira", 3, "", ["cetaria", "coronaria", "fumaria", "linaria", "lunaria", "parietaria", "saponaria", "serpentaria"]),
    Rule("(í|i)stico", 3, "", ["balístico", "ensaístico"]),
    Rule("ista", 3, "", ["batista", "ciclista", "fadista",
        "operista", "tenista", "verista"]),
    Rule("ado", 2, "", ["grado", "agrado"]),
    Rule("ato", 2, "", ["agnato"]),
    Rule("ido", 3, "", ["cándido", "cândido","consolido", "decidido", "duvido", "marido", "rápido"]),
    Rule("ida", 3, "", ["bastida", "dúbida", "dubida", "duvida", "ermida", "éxida", "guarida", "lapicida", "medida", "morida"]),
    Rule("ída", 3, "", []),
    Rule("ido", 3, "", []),
    Rule("udo", 3, "", ["estudo", "escuso"]),
    Rule("uda", 3, "", []),
    Rule("ada", 3, "", ["abada", "alhada", "allada", "pitada"]),
    Rule("dela", 3, "", ["cambadela", " cavadela", "forcadela", "erisipidela", "mortadela", "espadela", "fondedela", "picadela", "arandela", "candela", "cordela",
     "escudela", "pardela"]),
    Rule("ela", 3, "", ["canela", "capela", "cotela", "cubela", "curupela", "escarapela", "esparrela", "estela", "fardela", "flanela", "fornela",
     "franela", "gabela", "gamela", "gavela", "glumela", "granicela", "lamela", "lapela", "malvela", "manela", "manganela", "mexarela", "micela", "mistela", "novela",
     "ourela", "panela", "parcela", "pasarela", "patamela", "patela", "paxarela", "pipela", "pitela", "postela", "pubela", "restela", "sabela", "salmonela", "secuela",
     "sentinela", "soldanela", "subela", "temoncela", "tesela", "tixela", "tramela", "trapela", "varela", "vitela", "xanela", "xestela"]),
    Rule("(á|a)bel", 2, "", ["afábel","fiábel"]),
    Rule("íbel", 2, "", ["críbel", "imposíbel", "posíbel", "fisíbel", "falíbel"]),
    Rule("nte", 3, "", ["alimente", "adiante", "acrescente", "elefante", "frequente", "freqüente", "gigante", "instante", "oriente", "permanente",
     "posante", "possante", "restaurante"]),
    Rule("ncia", 3, "", []),
    Rule("nza", 3, "", []),
    Rule("acia", 3, "", ["acracia", "audacia", "falacia", "farmacia"]),
    Rule("icia", 3, "", ["caricia", "delicia", "ledicia", "malicia", " milicia", "noticia", "pericia", "presbicia", "primicia", "regalicia", "sevicia", "tiricia"]),
    Rule("iza", 3, "", ["alvariza", "baliza", "cachiza", "caniza", "cañiza", "carbaliza", "carriza", "chamariza",
     "chapiza", "fraguiza", "latiza", "longaniza", "mañiza", "nabiza", "peliza", "preguiza", "rabiza"]),
    Rule("exar", 3, "", ["palmexar"]),
    Rule("aci(ó|o)n", 2, "", ["aeración"]),
    Rule("ici(ó|o)n", 3, "", ["condición", "gornición", "monición", "nutrición", "petición", "posición", "sedición", "volición"]),
    Rule("ci(ó|o)n", 3, "t", []),
    Rule("si(ó|o)n", 3, "s", ["abrasión", "alusión"]),
    Rule("az(ó|o)n", 2, "", ["armazón"]),
    Rule("(ó|o)n", 3, "", ["abalón", "acordeón", "alción", "aldrabón", "alerón", "aliñón", "ambón", "bombón", "calzón",
     "campón", "canalón", "cantón", "capitón", "cañón", "centón", "ciclón", "collón", "colofón", "copón", " cotón", "cupón", "petón",
     "tirón", "tourón", "turón", "unción", "versión", "zubón", "zurrón"]),
    Rule("ona", 3, "", ["abandona", "acetona", "aleurona", "amazona", "anémona", "bombona", "cambona", "carona",
                "chacona", "charamona", "cincona", "condona", "cortisona", "cretona", "cretona", "detona", "estona", "fitohormona", "fregona",
                "gerona", "hidroquinona", "hormona", "lesiona", "madona", "maratona", "matrona", "metadona", "monótona", "neurona", "pamplona",
                "peptona", "poltrona", "proxesterona", "quinona", "quinona", "silicona", "sulfona"]),
    Rule("oa", 3, "", ["abandoa", "madroa", "barbacoa", "estoa", "airoa", "eiroa", "amalloa", "ámboa", "améndoa", "anchoa",
     "antinéboa", "avéntoa", "avoa", "bágoa", "balboa", "bisavoa", "boroa", "canoa", "caroa", "comadroa", "coroa", "éngoa", "espácoa", "filloa",
     "fírgoa", "grañoa", "lagoa", "lanzoa", "magoa", "mámoa", "morzoa", "noiteboa", "noraboa", "parañoa", "persoa", "queiroa", "rañoa", "táboa",
     "tataravoa", "teiroa"]),
    Rule("aco", 3, "", []),
    Rule("aca", 3, "", ["alpaca", "barraca", "bullaca", "buraca", "carraca", "casaca", "cavaca", "cloaca", "entresaca",
     "ervellaca", "espinaca", "estaca", "farraca", "millaca", "pastinaca", "pataca", "resaca", "urraca", "purraca"]),
    Rule("al", 4, "", ["afinal", "animal", "estatal", "bisexual", "bissexual", "desleal", "fiscal", "formal", "pessoal",
     "persoal", "liberal", "postal", "virtual", "visual", "pontual", "puntual", "homosexual", "heterosexual"]),
    Rule("dor", 2, "", ["abaixador"]),
    Rule("tor", 3, "", ["autor", "motor", "pastor", "pintor"]),
    Rule("or", 2, "", ["asesor", "assessor", "favor", "mellor", "melhor", "redor", "rigor", "sensor", "tambor", "tumor"]),
    Rule("ora", 3, "", ["albacora", "anáfora", "áncora", "apisoadora", "ardora", "ascospora", "aurora", "avéspora", "bitácora",
     "canéfora", "cantimplora", "catáfora", "cepilladora", "demora", "descalcificadora", "diáspora", "empacadora", "epífora", "ecavadora", "escora",
     "eslora", "espora", "fotocompoñedora", "fotocopiadora", "grampadora", "isícora", "lavadora", "lixadora", "macrospora", "madrépora", "madrágora",
     "masora", "mellora", "metáfora", "microspora", "milépora", "milpéndora", "nécora", " oospora", "padeadora", "pasiflora", "pécora", "píldora",
     "pólvora", "ratinadora", "rémora", "retroescavadora", "sófora", "torradora", "trémbora", "uredospora", "víbora", "víncora", "zoospora"]),
    Rule("aria", 3, "", ["libraría"]),
    Rule("axe", 3, "", ["aluaxe", "amaraxe", "amperaxe", "bagaxe", "balaxe", "barcaxe", "borraxe", "bescaxe", "cabotaxe",
     "carraxe", "cartilaxe", "chantaxe", "colaxe", "coraxe", "carruaxe", "dragaxe", "embalaxe", "ensilaxe", "epistaxe", "fagundaxe", "fichaxe",
     "fogaxe", "forraxe", "fretaxe", "friaxe", "garaxe", "homenaxe", "leitaxe", "liñaxe", "listaxe", "maraxe", "marcaxe", "maridaxe", "masaxe",
     "miraxe", "montaxe", "pasaxe", "peaxe", "portaxe", "ramaxe", "rebelaxe", "rodaxe", "romaxe", "sintaxe", "sondaxe", "tiraxe", "vantaxe", "vendaxe", "viraxe"]),
    Rule("dizo", 3, "", []),
    Rule("eza", 3, "", ["alteza", "beleza", "fereza", "fineza", "vasteza", "vileza"]),
    Rule("ez", 3, "", ["acidez", "adultez", "adustez", "avidez", "candidez", "mudez", "nenez", "nudez", "pomez"]),
    Rule("engo", 3, "", []),
    Rule("ego", 3, "", ["corego", "derrego", "entrego", "lamego", "sarego", "sartego"]),
    Rule("oso", 3, "", ["afanoso", "algoso", "caldoso", "caloso", "cocoso", "ditoso", "favoso", "fogoso", "lamoso",
        "mecoso", "mocoso", "precioso", "rixoso", "venoso", "viroso", "xesoso"]),
    Rule("osa", 3, "", ["mucosa", "glicosa", "baldosa", "celulosa", "isoglosa", "nitrocelulosa", "levulosa", "ortosa", "pectosa",
        "preciosa", "sacarosa", "serosa", "ventosa"]),
    Rule("ume", 3, "", ["agrume", "albume", "alcume", "batume", "cacume", "cerrume", "chorume", "churume", "costume",
     "curtume", "estrume", "gafume", "legume", "perfume", "queixume", "zarrume"]),
    Rule("ura", 3, "", ["albura", "armadura", "imatura", "costura"]),
    Rule("iñar", 3, "", []),
    Rule("il", 3, "", ["abril", "alfil", "anil", "atril", "badil", "baril", "barril", "brasil", "cadril", "candil",
     "cantil", "carril", "chamil", "chancil", "civil", "cubil", "dátil", "difícil", "dócil", "edil", "estéril", "fácil", "fráxil", "funil",
     "fusil", "grácil", "gradil", "hábil", "hostil", "marfil"]),
    Rule("esco", 4, "", []),
    Rule("isco", 4, "", []),
    Rule("ivo", 3, "", ["pasivo", "positivo", "passivo", "possessivo", "posesivo", "pexotarivo", "relativo"]),
    Rule("iva", 3, "", ["choiva", "conxuntiva", "cooperativa", "dáciva", "defensiva", "deriva", "diapositiva", "dioiva",
     "disxuntiva", "enxiva", "evasiva", "espectativa", "iniciativa", "invectiva", "inventiva", "lavativa", "leiva", "misiva", "ofensiva",
     "oliva", "perspectiva", "prospectiva", "recidivia", "rogativa", "saliva", "tentativa"]),
    Rule("és", 3, "", ["burgués"])
]


## VERB ENDINGS

VERBS = [
    Rule("aba", 2, "", []),
    Rule("abade", 2, "", []),
    Rule("ábade", 2, "", []),
    Rule("abamo", 2, "", []),
    Rule("ábamo", 2, "", []),
    Rule("aban", 2, "", []),
    Rule("che", 2, "", []),
    Rule("de", 2, "", []),
    Rule("n", 2, "", []),
    Rule("ndo", 2, "", []),
    Rule("ar", 2, "", ["azar","bazar","patamar"]),
    Rule("rade", 2, "", []),
    Rule("aramo", 2, "", []),
    Rule("arán", 2, "", []),
    Rule("aran", 2, "", []),
    Rule("árade", 2, "", []),
    Rule("aría", 2, "", []),
    Rule("ariade", 2, "", []),
    Rule("aríade", 2, "", []),
    Rule("arian", 2, "", []),
    Rule("ariamo", 2, "", []),
    Rule("aron", 2, "", []),
    Rule("ase", 2, "", []),
    Rule("asede", 2, "", []),
    Rule("ásede", 2, "", []),
    Rule("asemo", 2, "", []),
    Rule("ásemo", 2, "", []),
    Rule("asen", 2, "", []),
    Rule("avan", 2, "", []),
    Rule("aríamo", 2, "", []),
    Rule("assen", 2, "", []),
    Rule("ássemo", 2, "", []),
    Rule("eríamo", 2, "", []),
    Rule("êssemo", 2, "", []),
    Rule("iríamo", 3, "", []),
    Rule("íssemo", 3, "", []),
    Rule("áramo", 2, "", []),
    Rule("árei", 2, "", []),
    Rule("aren", 2, "", []),
    Rule("aremo", 2, "", []),
    Rule("aríei", 2, "", []),
    Rule("ássei", 2, "", []),
    Rule("ávamo", 2, "", []),
    Rule("êramo", 1, "", []),
    Rule("eremo", 1, "", []),
    Rule("eríei", 1, "", []),
    Rule("êssei", 1, "", []),
    Rule("íramo", 3, "", []),
    Rule("iremo", 3, "", []),
    Rule("iríei", 3, "", []),
    Rule("íssei", 3, "", []),
    Rule("issen", 3, "", []),
    Rule("endo", 1, "", []),
    Rule("indo", 3, "", []),
    Rule("ondo", 3, "", []),
    Rule("arde", 2, "", []),
    Rule("arei", 2, "", []),
    Rule("aria", 2, "", []),
    Rule("armo", 2, "", []),
    Rule("asse", 2, "", []),
    Rule("aste", 2, "", []),
    Rule("ávei", 2, "", []),
    Rule("erão", 1, "", []),
    Rule("erde", 1, "", []),
    Rule("erei", 1, "", []),
    Rule("êrei", 1, "", []),
    Rule("eren", 2, "", []),
    Rule("eria", 1, "", []),
    Rule("ermo", 1, "", []),
    Rule("este", 1, "", ["faroeste","agreste"]),
    Rule("íamo", 1, "", []),
    Rule("ian", 2, "", ["enfian", "eloxian", "ensaian"]),
    Rule("irde", 2, "", []),
    Rule("irei", 3, "", ["admirei"]),
    Rule("iren", 3, "", []),
    Rule("iria", 3, "", []),
    Rule("irmo", 3, "", []),
    Rule("isse", 3, "", []),
    Rule("iste", 4, "", []),
    Rule("iava", 1, "", ["ampliava"]),
    Rule("amo", 2, "", []),
    Rule("iona", 3, "", []),
    Rule("ara", 2, "", ["arara","prepara"]),
    Rule("ará", 2, "", ["alvará", "bacará", "bacarrá"]),
    Rule("are", 2, "", ["prepare"]),
    Rule("ava", 2, "", ["agrava"]),
    Rule("emo", 2, "", []),
    Rule("era", 1, "", ["acelera","espera"]),
    Rule("erá", 1, "", []),
    Rule("ere", 1, "", ["espere"]),
    Rule("íei", 1, "", []),
    Rule("in", 3, "", []),
    Rule("imo", 3, "", ["reprimo","intimo","íntimo","nimo","queimo","ximo"]),
    Rule("ira", 3, "", ["fronteira","sátira"]),
    Rule("ído", 3, "", []),
    Rule("irá", 3, "", []),
    Rule("tizar", 4, "", ["alfabetizar"]),
    Rule("izar", 3, "", ["organizar"]),
    Rule("itar", 5, "", ["acreditar","explicitar","estreitar"]),
    Rule("ire", 3, "", ["adquire"]),
    Rule("omo", 3, "", []),
    Rule("ai", 2, "", []),
    Rule("ear", 4, "", ["alardear","nuclear"]),
    Rule("uei", 3, "", []),
    Rule("uía", 5, "u", []),
    Rule("ei", 3, "", []),
    Rule("er", 1, "", ["éter","pier"]),
    Rule("eu", 1, "", ["chapeu"]),
    Rule("ia", 1, "", ["estória","fatia","acia","praia","elogia","mania","lábia","aprecia","polícia","arredia","cheia","ásia"]),
    Rule("ir", 3, "", []),
    Rule("iu", 3, "", []),
    Rule("eou", 5, "", []),
    Rule("ou", 3, "", []),
    Rule("i", 1, "", []),
    Rule("ede", 1, "", ["rede","bípede","céspede","parede","palmípede","vostede","hóspede","adrede"]),
    Rule("ei", 3, "", []),
    Rule("en", 2, "", []),
    Rule("erade", 1, "", []),
    Rule("érade", 1, "", []),
    Rule("eran", 2, "", []),
    Rule("eramo", 1, "", []),
    Rule("éramo", 1, "", []),
    Rule("erán", 1, "", []),
    Rule("ería", 1, "", []),
    Rule("eriade", 1, "", []),
    Rule("eríade", 1, "", []),
    Rule("eriamo", 1, "", []),
    Rule("erian", 1, "", []),
    Rule("erían", 1, "", []),
    Rule("eron", 1, "", []),
    Rule("ese", 1, "", []),
    Rule("esedes", 1, "", []),
    Rule("ésedes", 1, "", []),
    Rule("esemo", 1, "", []),
    Rule("ésemo", 1, "", []),
    Rule("esen", 1, "", []),
    Rule("êssede", 1, "", []),
    Rule("ía", 1, "", []),
    Rule("iade", 1, "", []),
    Rule("íade", 1, "", []),
    Rule("iamo", 1, "", []),
    Rule("ían", 1, "", []),
    Rule("iche", 1, "", []),
    Rule("ide", 1, "", []),
    Rule("irade", 3, "", []),
    Rule("írade", 3, "", []),
    Rule("iramo", 3, "", []),
    Rule("irán", 3, "", []),
    Rule("iría", 3, "", []),
    Rule("iriade", 3, "", []),
    Rule("iríade", 3, "", []),
    Rule("iriamo", 3, "", []),
    Rule("irian", 3, "", []),
    Rule("irían", 3, "", []),
    Rule("iron", 3, "", []),
    Rule("ise", 3, "", []),
    Rule("isede", 3, "", []),
    Rule("ísede", 3, "", []),
    Rule("isemo", 3, "", []),
    Rule("ísemo", 3, "", []),
    Rule("isen", 3, "", []),
    Rule("íssede", 3, "", []),
    Rule("tizar", 3, "", ["alfabetizar"]),
    Rule("ondo", 3, "", [])
]


## THEMATICAL VOWEL

THEMATIC = [
    Rule("gue", 2, "g", ["azougue", "dengue", "merengue", "nurague", "merengue", "rengue"]),
    Rule("que", 2, "c", ["alambique", "albaricoque", "abaroque", "alcrique", "almadraque", "almanaque", "arenque", "arinque", "baduloque", "ballestrinque", "betoque", "bivaque", "bloque", "bodaque", "bosque", "breque", "buque", "cacique", "cheque", "claque", "contradique", "coque", "croque", "dique", "duque", "enroque", "espeque", "estoque", "estoraque", "estraloque", "estrinque", "milicroque", "monicreque", "orinque", "arinque", "palenque", "parque", "penique", "picabeque", "pique", "psique", "raque", "remolque", "xeque", "repenique", "roque", "sotobosque", "tabique", "tanque", "toque", "traque", "truque", "vivaque", "xaque"]),
    Rule("a", 3, "", ["amasadela", "cerva"]),
    Rule("e", 3, "", ["marte"]),
    Rule("o", 3, "", ["barro", "fado", "cabo", "libro", "cervo"]),
    Rule("â", 3, "", []),
    Rule("ã", 3, "", ["Amanhã", "arapuã", "fã", "divã", "manhã"]),
    Rule("ê", 3, "", []),
    Rule("ô", 3, "", []),
    Rule("á", 3, "", []),
    Rule("é", 3, "", []),
    Rule("ó", 3, "", []),
    Rule("i", 3, "", []),
]