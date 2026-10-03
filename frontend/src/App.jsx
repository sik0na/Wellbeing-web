import { useEffect, useState } from "react"
import History from "./History"
import Chat from "./Chat.jsx"
import Calendar from "./Calendar.jsx"

function App(){
  const [loggedIn, setLoggedIn] = useState(null)

  const[username, setUsername] = useState("")
  const[password, setPassword] = useState("")
  const[error, setError] = useState("")
  const [savedCount, setSavedCount] = useState(0)

  const [lang, setLang] = useState(localStorage.getItem("lang") || "en")
  const [texts, setTexts] = useState({})

  useEffect(()=>{
    fetch("/api/me").then((response) => response.json())
    .then((data) => setLoggedIn(data.logged_in))
  }, [])

  useEffect(() => {
    fetch("/api/translations/" + lang)
    .then((response) => response.json())
    .then((data) => setTexts(data.texts))
    localStorage.setItem("lang", lang)
  }, [lang])

  function t(text, values = {}) {
    let result = texts[text] || text
    for (const key in values) {
      result = result.replace("{" + key + "}", values[key])
    }
    return result
  }
  async function login(event) {
    event.preventDefault()
    const response = await fetch("/api/login", {
      method:"post",
      headers: {"Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    })
    const data = await response.json()
    if (response.ok) {
      setLoggedIn(true)
      setError("")
    }else {
      setError(data.error)
    }
  }
  async function logout() {
    await fetch("/api/logout", {method: "post"})
    setLoggedIn(false)
  }

  const languageButtons = (
    <div className="language-buttons">
      <button type="button" onClick={() => setLang("en")} disabled={lang === "en"}>EN</button>
      <button type="button" onClick={() => setLang("hu")} disabled={lang === "hu"}>HU</button>
      <button type="button" onClick={() => setLang("mn")} disabled={lang === "mn"}>MN</button>
    </div>
  )

  if (loggedIn === null) return <p>Loading...</p>

  if (!loggedIn){
    return (
    <form onSubmit={login}>
            {languageButtons}
      <h1>{t("Log in")}</h1>
      {error && <p style={{color: "red"}}>{error}</p>}
      <input placeholder={t("Username")} value={username} onChange={(e) => setUsername(e.target.value)}/>
      <input placeholder={t("Password")} type="password" value={password} onChange={(e) => setPassword(e.target.value)}/>
      <button type="submit">{t("Log in")}</button>
    </form>
    )
  }

  return (
    <div>
            {languageButtons}
      <h1>{t("How are you today?")}</h1>
      <Chat t={t} lang={lang} onSaved = {() => setSavedCount(savedCount + 1)}/>
      <Calendar t={t} lang={lang} savedCount={savedCount} />
      <History t={t} savedCount = {savedCount}/>
      <button onClick={logout}>{t("Log out")}</button>
    </div>
  )
}

export default App