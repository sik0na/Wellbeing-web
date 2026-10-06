import { useEffect, useState } from "react"
import History from "./History"
import Chat from "./Chat.jsx"
import Calendar from "./Calendar.jsx"

const PAGES = ["home", "calendar", "habits", "activities", "profile"]
const PAGE_NAMES = {
  home: "Home",
  calendar: "Calendar",
  habits: "Activites",
  activities: "Activities",
  profile: "Profile",
}

function App(){
  const [loggedIn, setLoggedIn] = useState(null)

  const[username, setUsername] = useState("")
  const[password, setPassword] = useState("")
  const[error, setError] = useState("")
  const [savedCount, setSavedCount] = useState(0)
  const [mode, setMode] = useState("login")  
  const [page, setPage] = useState("home")    
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
    setPage("home")
  }

  
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

        {page === "home" && (
          <>
            <h1 className="hello">{t("How are you today?")}</h1>
            <Chat t={t} lang={lang} onSaved={() => setSavedCount(savedCount + 1)} />
          </>
        )}

        {page === "calendar" && (
          <>
            <Calendar t={t} lang={lang} savedCount={savedCount} />
            <History t={t} savedCount={savedCount} />
          </>
        )}

        {(page === "habits" || page === "activities") && (
          <div className="card">
            <h2>{t(PAGE_NAMES[page])}</h2>
            <p className="muted">{t("Coming soon")} 🌱</p>
          </div>
        )}

        {page === "profile" && (
          <div className="card">
            <h2>{t("Profile")}</h2>
            <button className="secondary full-width" onClick={logout}>{t("Log out")}</button>
          </div>
        )}
      </main>

      
      <nav>
        {PAGES.map((name) => (
          <button key={name} type="button" className={page === name ? "" : "secondary"} onClick={() => setPage(name)}>
            {t(PAGE_NAMES[name])}
          </button>
        ))}
      </nav>
    </>
  )
}

export default App