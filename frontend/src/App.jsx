import InputForm from "./InputForm"
import { useState } from "react"

function App() {
  const [results, setResults] = useState(null)
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <h1 className="text-3xl font-bold text-gray-900">MECAQC</h1>
      <p className="text-gray-500 mt-2">Multi-pollutant Emissions Calculator for Air Quality and Climate</p>
      <InputForm setResults={setResults} />
    </div>
  )
}

export default App