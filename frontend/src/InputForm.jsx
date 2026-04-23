import { useState } from 'react';

function InputForm({ setResults })
{
    const [formData, setFormData] = useState({
        state: "",
        capacity: "",
        annualGeneration: "",
        heatInput: "",
        baselineSO2: "",
        baselineNOx: "",
        baselinePM25: "",
        baselineVOC: "",
        baselineCO2: ""
    });

    function handleChange(e) {
        setFormData({ ...formData, [e.target.name]: e.target.value });  
    }

    async function handleSubmit(e) {
        e.preventDefault() // stops the browser from refreshing the page
  
        const response = await fetch("http://localhost:8000/scenario/run", 
        {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(
                {
                ...formData,
                capacity: parseInt(formData.capacity),
                annualGeneration: Number(formData.annualGeneration),
                baselineSO2: Number(formData.baselineSO2),
                baselineNOx: Number(formData.baselineNOx),
                baselinePM25: Number(formData.baselinePM25),
                baselineVOC: Number(formData.baselineVOC),
                baselineCO2: Number(formData.baselineCO2),
                }
            )
        })

        const data = await response.json()
        setResults(data)
    }

    return (
        <form onSubmit ={handleSubmit}>
            <input
                name="state"
                value={formData.state}
                onChange={handleChange}
                placeholder="e.g. WI"
            />
            <input
                name = "capacity"
                value={formData.capacity}
                onChange={handleChange}
                placeholder="e.g. 600 MW"
            />
            <input
                name = "annualGeneration"
                value={formData.annualGeneration}
                onChange={handleChange}
                placeholder="e.g. 3,066,000 MWh"
            />
            <input
                name="heatInput"
                value={formData.heatInput}
            onChange={handleChange}
            placeholder="e.g. 1598916 MMBtu/yr"
            />
            <input
                name = "baselineSO2"
                value={formData.baselineSO2}
                onChange={handleChange}
                placeholder="e.g. 11,000 MW"
            />
            <input
                name = "baselineNOx"
                value={formData.baselineNOx}
                onChange={handleChange}
                placeholder="e.g. 4,800 MW"
            />
            <input
                name = "baselinePM25"
                value={formData.baselinePM25}
                onChange={handleChange}
                placeholder="e.g. 820 MW"
            />
            <input
                name = "baselineVOC"
                value={formData.baselineVOC}
                onChange={handleChange}
                placeholder="e.g. 160 MW"
            />
            <input
                name = "baselineCO2"
                value={formData.baselineCO2}
                onChange={handleChange}
                placeholder="e.g. 2,820,000 MW"
            />

            <button type="submit">Submit</button>

        </form>
        
    )

    
}



export default InputForm;