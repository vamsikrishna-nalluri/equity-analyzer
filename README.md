# equity-analyzer
Stock's Fundamental and Technical Analysis

## Description
The stock analysis helps to make investment decision by getting the fundamental and technical details of the stock. 

This also helps to analyse the stock by AI, by providing the necessary or required information.

## pre-requisite:
Add ANTHROPIC_API_KEY to system environment. We don't want to have it as part of project .env file.

## Start Service
run `uvicorn equity_analyzer.main:app --reload --app-dir src`

## docs
URL : http://127.0.0.1:8000/docs