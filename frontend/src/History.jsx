import { useEffect, useState } from "react";

export default function History() {
    const [checkins, setCheckins] = useState([])

    useEffect(() => {
        fetch("/api/history").then((response) => response.json())
        .then((data) => setCheckins(data.checkins))

    }, [])

    return (
        <div>
            <h2>Your history</h2>

            {checkins.map((c) => (
                <p key={c.id}>
                     {c.created_at} · {c.chosen}: {c.text}
                </p>
            ))}
            {checkins.length === 0 && <p>No check-ins yet.</p>}
        </div>
    )
}