import { useEffect, useState } from "react";

export default function History({ savedCount, t }) {
    const [checkins, setCheckins] = useState([])

    useEffect(() => {
        fetch("/api/history").then((response) => response.json())
        .then((data) => setCheckins(data.checkins))

    }, [savedCount])

    return (
        <div>
            <h2>{t("Your history")}</h2>

            {checkins.map((c) => (
                <p key={c.id}>
                     {c.created_at} · {c.chosen}: {c.text}
                </p>
            ))}
            {checkins.length === 0 && <p>{t("No check-ins yet.")}</p>}
        </div>
    )
}