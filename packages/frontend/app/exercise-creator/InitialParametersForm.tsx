"use client"
import { useState, FC, useEffect } from 'react';

const ageToWeightAndHeight = {
    '1 hour': { weight: 3.5, height: 50 },
    '6 hours': { weight: 3.6, height: 50.2 },
    '12 hours': { weight: 3.7, height: 50.4 },
    '1 day': { weight: 3.8, height: 50.6 },
    '2 days': { weight: 4, height: 51 },
    '3 days': { weight: 4.2, height: 52 },
    '1 week': { weight: 4.5, height: 54 },
    '2 weeks': { weight: 5, height: 56 },
    '1 month': { weight: 5.7, height: 60 },
    '2 months': { weight: 6.5, height: 65 },
    '3 months': { weight: 7.5, height: 68 },
    '6 months': { weight: 8.5, height: 72 },
    '9 months': { weight: 9.2, height: 75 },
    '1 year': { weight: 10, height: 80 },
    '2 years': { weight: 12.5, height: 90 },
    '3 years': { weight: 14.5, height: 97 },
    '4 years': { weight: 16.5, height: 104 },
    '5 years': { weight: 18, height: 110 },
    '6 years': { weight: 20, height: 116 },
    '7 years': { weight: 22, height: 122 },
    '8 years': { weight: 24, height: 128 },
    '9 years': { weight: 26, height: 134 },
    '10 years': { weight: 28, height: 140 },
    '11 years': { weight: 30, height: 145 },
    '12 years': { weight: 32, height: 150 },
};
type AgeKey = keyof typeof ageToWeightAndHeight;

export interface InitialParametersFormState {
    age: AgeKey;
    sex: "male" | "female";
    description: string;
    simulationInstructions: string;
    weight: number;
    height: number;
}


type InitialParametersFormProps = {
    onSubmit: (data: InitialParametersFormState) => void;
    defaultData: InitialParametersFormState;
};

export function generateDefaultData(age: AgeKey = "3 years"): InitialParametersFormState {
    const defaultData = ageToWeightAndHeight[age];
    return {
        age: age,
        sex: "male",
        description: 'Accute sepsis with shallow breathing.',
        simulationInstructions: 'No response to IV fluids.',
        weight: defaultData.weight,
        height: defaultData.height
    }
}

const InitialParametersForm: FC<InitialParametersFormProps> = ({ onSubmit, defaultData }) => {
    const [formState, setFormState] = useState<InitialParametersFormState>(defaultData);
    const [isAdvancedVisible, setAdvancedVisible] = useState(false);

    useEffect(() => {
        const data = ageToWeightAndHeight[formState.age];
        setFormState(prev => ({ ...prev, ...data }));
    }, [formState.age]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        onSubmit(formState);
        // TODO: send data to the server, wait for a response, and then proceed to the next step.
    };

    const isFormValid = () => {
        // Check that all required fields are filled out
        return formState.age &&
            formState.description &&
            (formState.weight > 0) &&
            (formState.height > 0);
    };

    return (
        <div className="min-h-screen flex justify-center items-center">
            <div className="bg-white p-6 rounded-lg shadow-lg w-96">
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-600">Age</label>
                        <select
                            value={formState.age}
                            onChange={(e) => setFormState(prev => ({ ...prev, age: e.target.value as AgeKey }))}
                            className="mt-1 p-2 w-full border rounded-md"
                            required
                        >
                            {Object.keys(ageToWeightAndHeight).map(ageKey => (
                                <option key={ageKey} value={ageKey}>{ageKey}</option>
                            ))}
                        </select>
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-600">Sex</label>
                        <select
                            value={formState.sex}
                            onChange={(e) => setFormState(prev => ({ ...prev, sex: e.target.value as InitialParametersFormState['sex'] }))}
                            className="mt-1 p-2 w-full border rounded-md"
                            required
                        >
                            <option value="">Select...</option>
                            <option value="male">Male</option>
                            <option value="female">Female</option>
                            <option value="other">Other</option>
                        </select>
                    </div>

                    <div>
                        <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                            Patient's Initial Condition <span className="text-red-500">*</span>
                        </label>
                        <small className="text-red-500">Required</small>

                        <textarea
                            value={formState.description}
                            onChange={(e) => setFormState(prev => ({ ...prev, description: e.target.value }))}
                            className="mt-1 p-2 w-full border rounded-md"
                            rows={4}
                            placeholder="Eg. Acute sepsis"
                            required
                        ></textarea>
                    </div>


                    <div>
                        <label className="block text-sm font-medium text-gray-600">Simulation Instructions</label>
                        <textarea
                            value={formState.simulationInstructions}
                            onChange={(e) => setFormState(prev => ({ ...prev, simulationInstructions: e.target.value }))}
                            className="mt-1 p-2 w-full border rounded-md"
                            rows={4}
                            placeholder="Eg. Unknown allergy to paracetemol. No response to IV fluids."
                        ></textarea>
                    </div>

                    <div>
                        <button
                            type="button"
                            onClick={() => setAdvancedVisible(!isAdvancedVisible)}
                            className="text-blue-500 hover:underline"
                        >
                            {isAdvancedVisible ? 'Hide Advanced' : 'Show Advanced'}
                        </button>
                    </div>

                    <div className={`overflow-hidden transition-all duration-300 ${isAdvancedVisible ? 'max-h-60' : 'max-h-0'}`}>
                        <h4 className="text-lg font-medium">Advanced</h4>
                        <div className="space-y-2 mt-2">
                            <div>
                                <label className="block text-sm font-medium text-gray-600">Weight (kg)</label>
                                <input
                                    type="number"
                                    value={formState.weight}
                                    onChange={(e) => setFormState(prev => ({ ...prev, weight: parseFloat(e.target.value) }))}
                                    className="mt-1 p-2 w-full border rounded-md"
                                    required
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-gray-600">Height (cm)</label>
                                <input
                                    type="number"
                                    value={formState.height}
                                    onChange={(e) => setFormState(prev => ({ ...prev, height: parseFloat(e.target.value) }))}
                                    className="mt-1 p-2 w-full border rounded-md"
                                    required
                                />
                            </div>
                        </div>
                    </div>

                    <div>
                        <button
                            type="submit"
                            disabled={!isFormValid()}
                            title={!isFormValid() ? "Please fill out all required fields" : ""}
                            className={`bg-blue-500 hover:bg-blue-600 text-white p-2 rounded w-full ${!isFormValid() ? 'opacity-50 cursor-not-allowed' : ''}`}
                        >
                            Next
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default InitialParametersForm;
