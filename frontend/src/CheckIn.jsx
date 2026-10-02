import { useState } from "react"


async function post(url, data) {
    const response = await fetch(url, {
        method: "Post",
        headers: {"Content-Type": "application/json" },
        body: JSON.stringify(data),
    })
    return response.json()
}

export default function Checkin({ onSaved }) {
    const [text, setText] = useState("")
    const [suggestion, setSuggestion] = useState(null)
    const [message, setMessage] = useState("")
    const [saved, setSaved] = useState(false)

    async function checkIn(event) {
        event.preventDefault()
        setSuggestion(await post("/api/checkin", { text }))
    }

    async function confirm() {
        const data = await post("/api/message", { chosen: suggestion.emotion}) 
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
            {suggestion && !message && (
                <div>
                    <p>Does "{suggestion.emoji} {suggestion.name}" fir how you feel?</p>
                    <button onClick={confirm}>Yes, that fits</button>
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