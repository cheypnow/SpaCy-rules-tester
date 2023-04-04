import React, { useState } from 'react';
import { TextField, Button, Typography } from '@material-ui/core';

function MatchForm(props) {
    const [rules, setRules] = useState('');
    const [text, setText] = useState('');
    const [matchedTerms, setMatchedTerms] = useState([]);

    const handleSubmit = async (event) => {
        event.preventDefault();

        const response = await fetch('http://localhost:5001/api/match', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ rules, text })
        });

        const data = await response.json();
        setMatchedTerms(data);
    };

    return (
        <form onSubmit={handleSubmit}>
            <Typography variant="h6">Add rules and text to match</Typography>

            <TextField
                variant="outlined"
                margin="normal"
                required
                fullWidth
                id="rules"
                label="Rules"
                name="rules"
                multiline
                rows={4}
                value={rules}
                onChange={(event) => setRules(event.target.value)}
            />

            <TextField
                variant="outlined"
                margin="normal"
                required
                fullWidth
                id="text"
                label="Text"
                name="text"
                multiline
                rows={4}
                value={text}
                onChange={(event) => setText(event.target.value)}
            />

            <Button type="submit" variant="contained" color="primary">
                Match
            </Button>

            {matchedTerms.length > 0 && (
                <Typography variant="body1" component="p">
                    {matchedTerms.map((term, index) => (
                        <span key={index} style={{ backgroundColor: '#ffcc80' }}>
              {term}
            </span>
                    ))}
                </Typography>
            )}
        </form>
    );
}

export default MatchForm;