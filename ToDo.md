## Deploy
https://fly.io/


## Mapas IGN

- [CNIG-API](https://plataforma.idee.es/cnig-api)
  - [Ejemplos APICNIG](https://componentes.cnig.es/GaleriaEjemplos_APICNIG/)
    - [Visualizador1](https://componentes.cnig.es/GaleriaEjemplos_APICNIG/ejemplos/ejemploVisualizador01.html)
- [Cómo insertar un mapa con API CNIG](https://imasgal.com/insertar-un-mapa-con-api-cnig/)
- [github](https://github.com/IGN-CNIG/API-CNIG)

## Color

* [x] Change color (icon) based on points → done

## Alerts integration

* [ ] get summmit day alerts and show frequency and callsign from it
* [ ] warn if callsign is different from list

## Output format

* [ ] GeoJSON, try listing more atributes.

## Chasers
* [ ] Give chasers the possibility to calculate azimuths providing locator

## Popup

* [This popups displays better at mobile browser](https://componentes.cnig.es/GaleriaEjemplos_APICNIG/ejemplos/popupPersonalizadoOL01.html)

## Minimun requirements

* Expects xls (csv)  { summit, frequency, activator(s) }

The important (necessary) part is the Summit, activator is optional.

* [ ] Parse csv with summit list.
* [ ] Retreive summits from SOTA API.
* [ ] Add data from API to summit's CSV imported list.
* [ ] Calculate distance to summit's mother 
* [ ] given summits array, generate map


## Parser participants data

* [ ] Clase Summit:
    - Atributes: Summit reference, coordinates, activators, distance to summit's mum
    - Methods:
        - Distance to summit 
    - Retreives atributes data from API: `curl https://api2.sota.org.uk/api/summits/ea4/md-007`

## Icons

* [green-circle](https://icons8.com/icon/set/green-circle/emoji)
