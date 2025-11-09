# DataCoop25
Equip compost per Cristina Huanca, Lucas, Maria Siles i Clara Priego, estudiants d'enginyeria de dades de la UAB.


## Descripció del projecte
Aquest repositori conté el desenvolupament complet del repte de Caixa Enginyers, proposat en UAB The Hack 2025. L’objectiu ha estat identificar ubicacions prioritàries per a l’expansió territorial d’una entitat cooperativa, equilibrant criteris de sostenibilitat econòmica i impacte social.

## Procés de treball
**1. Recollida i neteja de dades**
Hem recopilat dades obertes de fonts com l’INE, OCDE i portals municipals.

Les variables clau inclouen: població, renda mitjana, cost de lloguer, presència d’entitats financeres, i indicadors d’inclusió.

S’han unificat i netejat les taules per municipi, utilitzant codis oficials (CPRO, CMUN) per facilitar el merge entre fonts.

**2. Construcció del model de priorització**
Hem creat un score compost que pondera criteris econòmics (renda, cost de lloguer) i socials (accés financer, població).

Aquest score s’ha normalitzat i calibrat per detectar municipis amb alta propensió a beneficiar-se d’un punt d’atenció cooperatiu.

**3. Geolocalització i visualització**
Per representar els resultats, hem integrat coordenades geogràfiques dels municipis des d’una base externa, evitant geocodificació manual.

Hem generat mapes de calor interactius amb Folium, que mostren el score i permeten explorar cada municipi amb popups informatius.

**4. Selecció de ubicacions prioritzades**
A partir del ranking de scores, hem seleccionat 3 municipis prioritaris per a acció immediata, tenint en compte:

Viabilitat econòmica (cost de lloguer)

Impacte social (baixa cobertura financera)

Capacitat operativa (població mínima)

**5. Model de propensió avançat**
Hem desenvolupat un model predictiu que estima l’evolució del score a 1, 3 i 5 anys vista.

S’han incorporat variables com la digitalització, el creixement demogràfic i el PIB local.

El model permet simular escenaris futurs i planificar l’expansió territorial de forma estratègica.

## Resultats
Dashboard interactiu amb mapes i gràfics que mostren la distribució territorial del score.

Informe executiu amb les 3 ubicacions prioritzades i les recomanacions estratègiques.

Model de propensió que pot ser reutilitzat per a noves zones o escenaris.
