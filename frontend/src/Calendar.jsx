import { useEffect, useState } from "react";

const LOCALES = {en: "en-GB", hu: "hu-HU"}

const MN_WEEKDAYS = ["Да", "Мя", "Лх", "Пү", "Ба", "Бя", "Ня"]

function toText(date) {
    const month = String(date.getMonth() + 1).padStart(2, "0")
    const day = String(date.getDate()).padStart(2, "0")
    return date.getFullYear() + "-" + month + "-" + day
}

export default function Calendar({ t, lang, savedCount }) {
    const today = new Date()
    const [year, setYear] = useState(today.getFullYear())
    const [month, setMonth] = useState(today.getMonth() + 1)
    const [weeks, setWeeks] = useState([])

    useEffect(() => {
        fetch(`/api/calendar/${year}/${month}`)
        .then((response) => response.json())
        .then((data) => setWeeks(data.weeks))
    }, [year, month, savedCount])

    function previousMonth() {
        if (month === 1) {
            setMonth(12)
            setYear(year-1)
        }else {
            setMonth(month - 1)
        }
    }

    function nextMonth() {
        if (month === 12) {
            setMonth(1)
            setYear(year + 1)
        }else {
            setMonth(month + 1)
        }
    }

    let title 
    let weekdays
    if (lang === "mn") {
        title = year + " оны " + month + "-р сар"     
        weekdays = MN_WEEKDAYS
    } else {
        const locale = LOCALES[lang]
        title = new Date(year, month - 1, 1).toLocaleDateString(locale, { month: "long", year: "numeric" })
        // 1 January 2024 was a Monday, so this gives Monday ... Sunday in the student's language
        weekdays = [0, 1, 2, 3, 4, 5, 6].map((i) =>
            new Date(2024, 0, 1 + i).toLocaleDateString(locale, { weekday: "short" }))
    }
    const todayText = toText(today)

    return (
        <div className="calendar">
            <h2>{t("Your mood calendar")}</h2>

            <div className="calendar-header">
                <button type="button" onClick={previousMonth} aria-label={t("Previous month")}>‹</button>
                <strong>{title}</strong>
                <button type="button" onClick={nextMonth} aria-label={t("Next month")}>›</button>
            </div>

            <div className="calendar-grid">
                {weekdays.map((name) => <div key={name} className="weekday">{name}

            </div>)}

            {weeks.flat().map((day, i) => {
                    if (day === null) return <div key={"empty-" + i} />  
                    let className = "day"
                    if (day.emotion) className += " mood-" + day.emotion
                    if (day.date === todayText) className += " today"
                    return (
                        <div key={day.date} className={className}>
                            <span className="day-number">{day.number}</span>
                            <span className="day-emoji">{day.emoji}</span>
                        </div>
                    )
                })}
            </div>
        </div>
    )
}
