# MECAQC
### Multi-pollutant Emissions Calculator for Air Quality and Climate

A full-stack web application that models four regulatory transition scenarios for coal-fired power facilities, producing monetized health and climate impact estimates across multiple pollutant types. Developed as a member of the Holloway Group at the University of Wisconsin–Madison, a NASA-affiliated atmospheric science research lab. This application implements and operationalizes the modeling framework from Wu et al. (2024).

> Based on: Wu, S., et al. (2024). Characterizing multi-pollutant emission impacts of sulfur reduction strategies from coal power plants. *Environmental Research Letters.*

---

## Features

- Models four transition scenarios: Business as Usual (BAU), Gas Transition (GT), Renewables Transition (RT), and Add-on Controls (AC)
- Calculates emissions changes across SO₂, NOₓ, PM₂.₅, VOC, and CO₂
- Produces annualized health and climate benefit estimates using EPA and EIA monetization factors
- State-specific cost adjustment logic based on EPA CAMPD and EIA reference datasets
- React frontend with real-time results rendering

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, Tailwind CSS |
| Backend | FastAPI, Python |
| Validation | Pydantic |
| Data sources | EPA CAMPD, EIA, Wu et al. 2024 |

---

## Project Structure

```
mecaqc/
├── backend/
│   ├── main.py           # FastAPI app and routes
│   ├── calculator.py     # Scenario calculation engine
│   ├── mock_data.py      # Constants and state lookup tables
│   └── schema.py         # Pydantic request/response schemas
├── src/
│   ├── App.jsx           # Root component, owns global state
│   ├── InputForm.jsx     # 9-field facility input form
│   └── ResultsPanel.jsx  # Scenario cards, charts, financials
├── public/
├── package.json
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+

### Backend

```bash
# From the project root
cd backend
pip install fastapi uvicorn pydantic

# Start the server
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

### Frontend

```bash
# From the project root
npm install
npm run dev
```

The app will be available at `http://localhost:5173`.

---

## API

### `POST /scenario/run`

Accepts facility-level inputs and returns cost-benefit outputs for all four scenarios.

**Request body**

```json
{
  "state": "AL",
  "capacity": 403,
  "heatInput": 1598916,
  "annualGeneration": 166714,
  "baselineSO2": 953,
  "baselineNOx": 227,
  "baselinePM25": 71.6,
  "baselineVOC": 4.1,
  "baselineCO2": 164046
}
```

**Response**

Returns scenario results for BAU, GT, RT, and AC including net benefit, total annual cost (TAC), and per-pollutant emission changes.

---

## Scenarios

| Scenario | Description | Status |
|---|---|---|
| BAU | Business as Usual | ✅ Verified |
| GT | Gas Transition | ✅ Verified |
| RT | Renewables Transition | ✅ Verified |
| AC | Add-on Controls | 🚧 Cost model in progress |

---

## Methodology

Emissions and cost calculations follow the peer-reviewed methodology from:

> Wu, S., et al. (2024). Health and climate benefits of different energy transition scenarios for coal-fired power plants in the United States. *Environmental Research Letters.*

Cost factors are sourced from EPA and EIA datasets and adjusted by state using regional multipliers. All costs are reported in **2020 dollars**.

---

## Acknowledgements

Developed as part of the [Holloway Group](https://hollowaygroup.org) at the University of Wisconsin–Madison, a NASA-affiliated atmospheric science research lab. Special thanks to Dr. Xinran Wu, Dr. Tracey Holloway, and Vedaa Vandavasi.
