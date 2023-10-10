import { FullABCDE } from "@/src/api";


const ABCDERenderer: React.FC<{
    abcdeData: FullABCDE;
    onChange: (key: keyof FullABCDE, value: string) => void;
}> = ({ abcdeData, onChange }) => {
    return (
        <div>
            {Object.entries(abcdeData).map(([key, value]) => (
                <div key={key} style={{display: "flex", gap: "0.5rem"}}>
                    <strong>{key}:</strong>
                    <input
                        style={{flexGrow: 1}}
                        type="text"
                        value={value ?? ''}
                        onChange={(e) => onChange(key as keyof FullABCDE, e.target.value)}
                    />
                </div>
            ))}
        </div>
    );
};

export default ABCDERenderer;