import React, {useState} from "react";

const MatchForm = () => {
    const matchUrl = 'http://localhost:5001/api/match';
    const [rules, setRules] = useState([{label: "", rule: ""}]);
    const [text, setText] = useState("");
    const [highlightedText, setHighlightedText] = useState("");

    const handleSubmit = (event) => {
        event.preventDefault();
        const ruleData = rules.map((r) => {
            return {
                label: r.label,
                patterns: r.rule,
            };
        });

        fetch(matchUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                text,
                rules: ruleData,
            }),
        })
            .then((response) => {
                response.json().then(
                    (data) => {
                        setHighlightedText(data.highlighted_text)
                    }
                )
            })
            .catch((error) => {
                console.error("Error:", error);
            });
    };

    const addRule = () => {
        const newRule = {label: "", rule: ""};
        setRules([...rules, newRule]);
    };

    const handleRuleChange = (e, index) => {
        const {name, value} = e.target;
        const newRules = [...rules];
        newRules[index][name] = value;
        setRules(newRules);
    };

    const handleTextChange = (e) => {
        setText(e.target.value);
    };

    return (
        <div>
            <h2>Match Form</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="text">Text:</label>
                    <textarea name="text" id="text" onChange={handleTextChange}/>
                </div>
                <div>
                    <label htmlFor="rules">Rules:</label>
                    {rules.map((rule, index) => (
                        <div key={index}>
                            <input
                                type="text"
                                placeholder="Label"
                                name="label"
                                value={rule.label}
                                onChange={(e) => handleRuleChange(e, index)}
                            />
                            <input
                                type="text"
                                placeholder="Pattern"
                                name="rule"
                                value={rule.rule}
                                onChange={(e) => handleRuleChange(e, index)}
                            />
                        </div>
                    ))}
                    <button type="button" onClick={addRule}>
                        Add Rule
                    </button>
                </div>
                <div>
                    <button type="submit">Submit</button>
                </div>
            </form>
            <div dangerouslySetInnerHTML={{__html: highlightedText}}/>
        </div>
    );
};

export default MatchForm;
