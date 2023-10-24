import React, { useState } from 'react';

export interface FunctionDefinition {
  function_name: string;
  params: string[];
}

interface FunctionSelectorProps {
  functions: FunctionDefinition[];
  onSubmit: (function_call: string) => void;
}

const FunctionSelector: React.FC<FunctionSelectorProps> = ({ functions, onSubmit }) => {
    const [selectedFunction, setSelectedFunction] = useState<FunctionDefinition | null>(null);
    const [paramValues, setParamValues] = useState<string[]>([]);
  
    const handleFunctionChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
      const functionName = event.target.value;
      const func = functions.find(f => f.function_name === functionName);
      if (func) {
        setSelectedFunction(func);
        setParamValues(new Array(func.params.length).fill(''));
      }
    };
  
    const handleParamChange = (index: number, value: string) => {
      const newParamValues = [...paramValues];
      newParamValues[index] = value;
      setParamValues(newParamValues);
    };
  
    const handleKeyPress = (event: React.KeyboardEvent<HTMLInputElement>) => {
      if (event.key === 'Enter') {
        handleSubmit();
      }
    };
  
    const handleSubmit = () => {
      if (!selectedFunction) return;
      onSubmit(`${selectedFunction.function_name}(${paramValues.join(', ')})`);
    };
  
    return (
      <div className="p-4">
        <select onChange={handleFunctionChange} className="mb-4 p-2 border rounded bg-gray-700">
          <option value="">Select a function</option>
          {functions.map(func => (
            <option key={func.function_name} value={func.function_name}>
              {func.function_name}
            </option>
          ))}
        </select>
  
        {selectedFunction && selectedFunction.params.map((param, index) => (
          <div key={param} className="mb-2">
            <label className="mr-2">{param}:</label>
            <input
              type="text"
              value={paramValues[index]}
              onChange={e => handleParamChange(index, e.target.value)}
              onKeyPress={handleKeyPress}
              className="p-2 border rounded bg-gray-700 white"
            />
          </div>
        ))}
        <button onClick={handleSubmit} className="p-2 border rounded bg-gray-700 white">
          Submit
        </button>
      </div>
    );
  }
  

export default FunctionSelector;
