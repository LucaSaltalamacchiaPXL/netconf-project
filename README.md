# NETCONF/YANG Automatisatie Project

## Overzicht
Dit project automatiseert de configuratie van Cisco IOS-XE routers met behulp van **NETCONF** en **YANG**. Het doel is om netwerkconfiguraties snel, herhaalbaar en foutloos uit te voeren, gebruikmakend van één centrale bron van waarheid.

## Doel
- Vereenvoudigen van routerconfiguratie
- Verminderen van menselijke fouten bij handmatige configuraties
- Creëren van een end-to-end geautomatiseerde workflow voor netwerkbeheer
- Integratie met GitHub als versiebeheer en centrale configuratiebron

## Wat is gedaan
### 1. config.xml
- Bevat de YANG-compatibele configuratie voor de router
- Gehost op GitHub zodat scripts automatisch de laatste versie downloaden

### 2. Python Scripts
- `deploy.py`
  - Downloadt automatisch de configuratie van GitHub
  - Verbindt met de router via NETCONF
  - Deployt de configuratie naar de `running` datastore
  - Valideert de configuratie vóór en na deployment en geeft feedback in de terminal
- `test_netconf.py`
  - Verifieert verbinding met de router
  - Test deploy-functionaliteit in een veilige testomgeving

### 3. GitHub Repository
- Centrale bron van waarheid voor alle configuraties
- Volledige versiecontrole voor scripts en configuraties
- Documentatie en workflow overzicht (optioneel: flowchart)

## End-to-End Workflow
1. Configuratie wordt beheerd in `config.xml` op GitHub
2. Python script `deploy.py` downloadt config en verbindt met de router
3. Deploy naar de router gebeurt automatisch via NETCONF
4. Script valideert de deploy door running-config op te halen en te vergelijken
5. Eventuele fouten of waarschuwingen worden direct weergegeven in de terminal
6. Documentatie en flowchart maken het proces inzichtelijk

## Voordelen van de automatisatie
- Snelle en consistente configuratie van routers
- Vermindering van menselijke fouten
- Herhaalbare en schaalbare oplossing voor meerdere routers
- Integratie met GitHub voor versiebeheer en samenwerking
- Mogelijkheid om te valideren vóór en na deployment

## Flowchart
Een visueel overzicht van de end-to-end workflow kan hier worden toegevoegd:

<img width="542" height="1261" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/a1117e8a-463b-458c-876d-2ac8ad6242a1" />
