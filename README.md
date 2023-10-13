# SmartCatToy


… is a toy controlled via a webapp to entertain our feline friends during our absence.

The idea behind this project is to provide a cheap alternative to expensive toys, with which you can provide entertainment for lonley single cats in flats.

## Project Team

Turpal-Ali Iliev
Armin Mühlfellner

## Must Have

- Spherical Toy
    - Moves around
    - Can receive input via network
- mobile App
    - connect toy to mobile app
    - control toy remotely
    - provides autopilot mode
- Back End
    - receive Data from App
    - send Data to Mobile app
- Database
    - Store Data from Backend
- Infrastructure
    - Running nodejs
    - Running database
    - reachable via internet

## Nice to Have

- replace autopilot (random generator) via inteligent movement detection
- add tail to toy for more interaction
- add sounds to toy
- add camera feed to app
- login (Database necessary)

## Technical Overview

Mobile App → Ionic Framework to develop webapp

Back End → NodeJS, Express, Sequelize 

Database system -> MS SQL

Hardware on Toy -> Raspberry Pi, Arduino, Sensors + Motors

Case for Toy -> Modelled and printed via 3D Printer
