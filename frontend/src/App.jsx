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
  const [mode, setMode] = useState("login")   // the form: "login" or "signup"

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
  // The same form logs in OR signs up, depending on mode
  async function login(event) {
    event.preventDefault()
    const response = await fetch(mode === "login" ? "/api/login" : "/api/signup", {
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

  // The EN · HU · MN switch: one pill, the chosen language is "active"
  const languageButtons = (
    <div className="lang-switch">
      {["en", "hu", "mn"].map((code) => (
        <button key={code} type="button" className={lang === code ? "active" : ""} onClick={() => setLang(code)}>
          {code.toUpperCase()}
        </button>
      ))}
    </div>
  )

  
  const topbar = (
    <header className="topbar">
      <span className="logo">
        <img src="/logo.png" alt="" className="logo-img"/>PAUSE
      </span>
      {languageButtons}
    </header>
  )

  if (loggedIn === null) return <p className="loading">Loading…</p>

  if (!loggedIn){
    const isLogin = mode === "login"
    return (
      <>
        {topbar}
        <main>
          <div className="welcome-emojis" aria-hidden="true">
            <span>
              <img src="/logo.png" alt="" className="welcome-logo"/>
            </span>
          </div>

          <form className="card auth-card" onSubmit={login}>
            <h1>{isLogin ? t("Welcome back") : t("Create your account")}</h1>
            <p className="muted">{t("Your check-ins are private to your account.")}</p>
            {error && <p className="error">{t(error)}</p>}

            <label htmlFor="username">{t("Username")}</label>
            <input id="username" value={username} autoComplete="username" onChange={(e)=>setUsername(e.target.value)} />
            <label htmlFor="password">{t("Password")}</label>
            <input id="password" type="password" value={password}
                autoComplete={isLogin ? "current-password" : "new-password"}
                onChange={(e) => setPassword(e.target.value)} />
            <button type="submit">{isLogin ? t("Log in") : t("Sign up")}</button>

            <p className="switch-text">{isLogin ? t("New here?") : t("Already have an account?")}{" "}
              <button type="button" className="link-button" onClick={()=> {setMode(isLogin ? "signup" : "login") ; setError("") }}>{isLogin ? t("Create an account") : t("Log in")}</button>
            </p>
          </form>
        </main>
      </>
    )
  }

  return (
    <>
      {topbar}
      <main>
        <h1 className="hello">{t("How are you today?")}</h1>
        <Chat t={t} lang={lang} onSaved = {() => setSavedCount(savedCount + 1)}/>
        <Calendar t={t} lang={lang} savedCount={savedCount} />
        <History t={t} savedCount = {savedCount}/>
        <button className="secondary full-width" onClick={logout}>{t("Log out")}</button>
      </main>
    </>
  )
}

export default App