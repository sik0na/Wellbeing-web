// History.jsx - the student's own check-ins, newest first.
// Each one has a round emoji in the soft colour of its mood.

import { useEffect, useState } from "react"

export default function History({ savedCount, t }) {
    const [checkins, setCheckins] = useState([])

    // Load again after a new check-in was saved
    useEffect(() => {
        fetch("/api/history")
            .then((response) => response.json())
            .then((data) => setCheckins(data.checkins))
    }, [savedCount])

    return (
        <div className="card">
            <h2>{t("Your history")}</h2>

            {checkins.length === 0 && <p className="muted">{t("No check-ins yet.")}</p>}

            <ul className="history-list">
                {checkins.map((c) => (
                    <li key={c.id}>
                        <span className={"history-emoji mood-" + c.chosen}>{c.emoji}</span>
                        <div>
                            <p className="history-text">{c.text}</p>
                            <span className="history-date">{c.created_at}</span>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    )
}
