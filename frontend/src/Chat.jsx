
import { useEffect, useState } from "react"


async function post(url, data) {
    const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    })
    return response.json()
}

let nextId = 1   

export default function Chat({ onSaved, t, lang}) {
    const [messages, setMessages] = useState([
        { id: 0, from: "bot", text: "Hi! How are you feeling today?" },
    ])
    const [input, setInput] = useState("")
    const [emotions, setEmotions] = useState([])
    const [checkin, setCheckin] = useState({})  

    
    useEffect(() => {
        fetch("/api/emotions?lang=" + lang)
            .then((response) => response.json())
            .then((data) => setEmotions(data.emotions))
    }, [lang])

    
    function add(...newMessages) {
        const withIds = newMessages.map((m) => ({ id: nextId++, ...m }))
        setMessages((old) => [...old, ...withIds])
    }

    
    function markUsed(id) {
        setMessages((old) => old.map((m) => (m.id === id ? { ...m, used: true } : m)))
    }

    
    async function send(event) {
        event.preventDefault()
        const text = input.trim()
        if (text === "") return

        add({ from: "user", text })
        setInput("")
        const answer = await post("/api/checkin", { text, lang})
        setCheckin({ text, predicted: answer.emotion })
        add(
                        { from: "bot", text: 'Does "{emotion}" fit how you feel?', values: { emotion: answer.emoji + " " + answer.name } },
            { type: "choices", suggestion: answer },
        )
    }

    
    async function choose(key, cardId) {
        markUsed(cardId)
        const emotion = emotions.find((e) => e.key === key)
        add({ from: "user", text: emotion.emoji + " " + emotion.name })
        setCheckin((old) => ({ ...old, chosen: key }))

        const data = await post("/api/message", { chosen: key, lang})
        add(
            { from: "bot", text: data.message },
            { type: "save" },
        )
    }

    
    async function save(cardId) {
        markUsed(cardId)
        await post("/api/save", checkin)
        add({ from: "bot", text: "Saved ✓ Anything else on your mind?" })
        onSaved()
    }

    function skip(cardId) {
        markUsed(cardId)
        add({ from: "bot", text: "Okay, not saved. Anything else on your mind?" })
    }

    return (
        <div className="chat">
            <div className="chat-log">
                {messages.map((m) => (
                    <Message key={m.id} message={m} emotions={emotions} t={t}
                             onChoose={choose} onSave={save} onSkip={skip} />
                ))}
            </div>

            <form className="chat-input" onSubmit={send}>
                <input value={input} onChange={(e) => setInput(e.target.value)} placeholder={t("Type a message…")} />
                <button type="submit">{t("Send")}</button>
            </form>
        </div>
    )
}


function Message({ message, emotions, t,  onChoose, onSave, onSkip }) {
    if (message.type === "choices") {
        const s = message.suggestion
        return (
            <div className="chat-card">
                <button disabled={message.used} onClick={() => onChoose(s.emotion, message.id)}>
                    <p>{t("Yes")}, {s.emoji} {s.name}</p>
                </button>
                <p>{t("Or pick another:")}</p>
                {emotions.filter((e) => e.key !== s.emotion).map((e) => (
                    <button key={e.key} disabled={message.used} onClick={() => onChoose(e.key, message.id)}>
                        {e.emoji} {e.name}
                    </button>
                ))}
            </div>
        )
    }

    if (message.type === "save") {
        return (
            <div className="chat-card">
                                <button disabled={message.used} onClick={() => onSave(message.id)}>{t("Save this check-in")}</button>
                <button disabled={message.used} onClick={() => onSkip(message.id)}>{t("No thanks")}</button>
            </div>
        )
    }

        const text = message.from === "bot" ? t(message.text, message.values) : message.text
    return <div className={"bubble " + message.from}>{text}</div>
}