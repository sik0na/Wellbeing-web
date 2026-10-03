// Chat.jsx - the check-in as a chat.
// The whole conversation is ONE list in state (messages).
// To show something new, we add it to the list, and React draws it.

import { useEffect, useState } from "react"


async function post(url, data) {
    const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    })
    return response.json()
}

let nextId = 1   // every message needs a different id (for React's key)

// t:    translates the fixed texts (from App.jsx)
// lang: "en", "hu" or "mn", sent to Flask so emotion names and messages come in that language
export default function Chat({ onSaved, t, lang }) {
    const [messages, setMessages] = useState([
        { id: 0, from: "bot", text: "Hi! How are you feeling today?" },
    ])
    const [input, setInput] = useState("")
    const [emotions, setEmotions] = useState([])
    const [checkin, setCheckin] = useState({})   // the check-in we are building: text, predicted, chosen

    // Load the 7 emotions (in the student's language). Again when the language changes.
    useEffect(() => {
        fetch("/api/emotions?lang=" + lang)
            .then((response) => response.json())
            .then((data) => setEmotions(data.emotions))
    }, [lang])

    // Add one or more messages to the end of the list
    function add(...newMessages) {
        const withIds = newMessages.map((m) => ({ id: nextId++, ...m }))
        setMessages((old) => [...old, ...withIds])
    }

    // Grey out a card after it was answered, so it can't be clicked twice
    function markUsed(id) {
        setMessages((old) => old.map((m) => (m.id === id ? { ...m, used: true } : m)))
    }

    // Step 1: the student sends a message, the model guesses
    async function send(event) {
        event.preventDefault()
        const text = input.trim()
        if (text === "") return

        add({ from: "user", text })
        setInput("")
        const answer = await post("/api/checkin", { text, lang })
        setCheckin({ text, predicted: answer.emotion })
        add(
            { from: "bot", text: 'Does "{emotion}" fit how you feel?', values: { emotion: answer.emoji + " " + answer.name } },
            { type: "choices", suggestion: answer },
        )
    }

    // Step 2: the student picks an emotion (the guess or another one)
    async function choose(key, cardId) {
        markUsed(cardId)
        const emotion = emotions.find((e) => e.key === key)
        add({ from: "user", text: emotion.emoji + " " + emotion.name })
        setCheckin((old) => ({ ...old, chosen: key }))

        const data = await post("/api/message", { chosen: key, lang })
        add(
            { from: "bot", text: data.message },
            { type: "save" },
        )
    }

    // Step 3: save or skip
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
        <div className="card">
            <div className="chat-log">
                {messages.map((m) => (
                    <Message key={m.id} message={m} emotions={emotions} t={t}
                             onChoose={choose} onSave={save} onSkip={skip} />
                ))}
            </div>

            <form className="chat-input" onSubmit={send}>
                <input value={input} onChange={(e) => setInput(e.target.value)} placeholder={t("Type a message…")} />
                {/* a round button with an arrow drawn in SVG */}
                <button type="submit" className="send-button" aria-label={t("Send")}>
                    <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" fill="none" stroke="currentColor"
                         strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round"><path d="M5 12h14M13 6l6 6-6 6" /></svg>
                </button>
            </form>
        </div>
    )
}

// One item of the list: a bubble, or a card with buttons
function Message({ message, emotions, t, onChoose, onSave, onSkip }) {
    if (message.type === "choices") {
        const s = message.suggestion
        return (
            <div className="choices">
                <button disabled={message.used} onClick={() => onChoose(s.emotion, message.id)}>
                    ✓ {t("Yes")}, {s.emoji} {s.name}
                </button>
                <p>{t("Or pick another:")}</p>
                {emotions.filter((e) => e.key !== s.emotion).map((e) => (
                    <button key={e.key} className="choice" disabled={message.used} onClick={() => onChoose(e.key, message.id)}>
                        {e.emoji} {e.name}
                    </button>
                ))}
            </div>
        )
    }

    if (message.type === "save") {
        return (
            <div className="choices">
                <button disabled={message.used} onClick={() => onSave(message.id)}>{t("Save this check-in")}</button>
                <button className="secondary" disabled={message.used} onClick={() => onSkip(message.id)}>{t("No thanks")}</button>
            </div>
        )
    }

    // Bot texts are translated when they are DRAWN, so switching language changes the whole chat.
    // The student's own words are never translated.
    const text = message.from === "bot" ? t(message.text, message.values) : message.text
    return <div className={"bubble " + message.from}>{text}</div>
}
