import React, {useState} from "react";
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Divider from '@material-ui/core/Divider';
import Box from '@material-ui/core/Box';

import './MatchForm.css'

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

    const deleteRule = (index) => {
        const updatedRules = [...rules];
        updatedRules.splice(index, 1);
        setRules(updatedRules);
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
        <div className="main-form">
            <h1>SpaCy rules tester</h1>
            <form className="rules-form" onSubmit={handleSubmit}>
                <div>
                    <h2>Rules:</h2>
                    {rules.map((rule, index) => (
                        <div className="rule-and-pattern-block" key={index}>
                            <div className="rule-label-block">
                                <TextField
                                    name="label"
                                    type="text"
                                    variant="outlined"
                                    placeholder="Label"
                                    value={rule.label}
                                    onChange={(e) => handleRuleChange(e, index)}
                                />
                                <Button disabled={rules.length <= 1} className="delete-rule-button"
                                        onClick={deleteRule}>
                                    Delete
                                </Button>
                            </div>
                            <div>
                                <TextField
                                    className="pattern-text"
                                    name="rule"
                                    type="text"
                                    multiline
                                    variant="outlined"
                                    value={rule.rule}
                                    onChange={(e) => handleRuleChange(e, index)}
                                />
                            </div>
                            <Divider/>
                        </div>
                    ))}
                    <Button variant="outlined" type="button" onClick={addRule}>
                        Add Rule
                    </Button>
                </div>
                <div>
                    <h2>Text:</h2>
                    <TextField
                        className="text-input"
                        name="text"
                        id="text"
                        multiline
                        variant="outlined"
                        onChange={handleTextChange}
                    />
                </div>
                <div>
                    <Button variant="contained" type="submit">Submit</Button>
                </div>
                <div className="scapy-response-text" dangerouslySetInnerHTML={{__html: highlightedText}}/>
            </form>
        </div>
    );
};

export default MatchForm;
