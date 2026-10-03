import { useState, useEffect } from "react"


async function post(url, data) {
    const response = await fetch(url, {
        method: "POST",
        headers: {"Content-Type": "application/json" },
        body: JSON.stringify(data),
    })
    return response.json()
}

export default function CheckIn({ onSaved }) {
    const [text, setText] = useState("")
    const [suggestion, setSuggestion] = useState(null)
    const [emotions, setEmotions] = useState([])
    const [picking, setPicking] = useState(false)
    const [chosen, setChosen] = useState("")
    const [message, setMessage] = useState("")
    const [saved, setSaved] = useState(false)
    
    useEffect(() => {
        fetch("/api/emotions").then((response) => response.json())
        .then((data) => setEmotions(data.emotions))
    }, [])

    async function checkIn(event) {
        event.preventDefault()
        setSuggestion(await post("/api/checkin", { text }))
    }

    async function choose(key) {
        setChosen(key)
        setPicking(false)
        const data = await post("/api/message", { chosen: key })
        setMessage(data.message)
    }

    async function save() {
        await post("/api/save", {text, predicted: suggestion.emotion, chosen: suggestion.emotion})
        setSaved(true)
        onSaved()
    }
    return (
        <div>
            <form onSubmit={checkIn}>
                <textarea value={text} onChange={(e) => setText(e.target.value)} placeholder="How are you feeling?"/>
                    <button type="submit">Check in</button>

            </form>

            {suggestion && !message && !picking && (
                <div>
                    <p>Does "{suggestion.emoji} {suggestion.name}" fit how you feel?</p>
                    <button onClick={() => choose(suggestion.emotion)}>Yes, that fits</button>
                    <button onClick={() => setPicking(true)}>No, pick another</button>
                </div>
            )}

            {picking &&(
                <div>
                    <p>How do you feel?</p>
                    {emotions.map((emotion) => (
                        <button key = {emotion.key} onClick = {()=> choose(emotion.key)}>{emotion.emoji} {emotion.name}</button>
                    ))}
                </div>
            )}

            {message && (
                <div>
                    <p>{message}</p>
                    {saved ? <p>Saved</p> : <button onClick={save}>Save this check-in</button>}
                </div>
            )}
        </div>
    )
}