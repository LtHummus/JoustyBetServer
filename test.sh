#!/bin/bash

#curl -X POST localhost:5000/player-signup -H "Content-Type: application/json" -d '{"name":"Hexicube"}'
#curl -X POST localhost:5000/player-signup -H "Content-Type: application/json" -d '{"name":"KrazyCaley"}'
#curl -X POST localhost:5000/player-signup -H "Content-Type: application/json" -d '{"name":"aforgottentune"}'
curl -X POST localhost:5000/register-bet -H "Content-Type: application/json" -d '{"name":"aforgottentune", "guess":"BLUE"}'
curl -X POST localhost:5000/register-bet -H "Content-Type: application/json" -d '{"name":"KrazyCaley", "guess":"BLUE"}'
curl -X POST localhost:5000/register-bet -H "Content-Type: application/json" -d '{"name":"Hexicube", "guess":"PINK"}'
