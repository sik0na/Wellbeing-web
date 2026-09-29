import { useEffect, useState } from "react"

function App(){
  const [loggedIn, setLoggedIn] = useState(null)

  const[username, setUsername] = useState("")
  const[password, setPassword] = useState("")
  const[error, setError] = useState("")


  useEffect(()=>{
    fetch("/api/me").then((response) => response.json())
    .then((data) => setLoggedIn(data.logged_in))
  }, [])

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
  if (loggedIn === null) return <p>Loading...</p>

  if (!loggedIn){
    return (
    <form onSubmit={login}>
      <h1>Log in</h1>
      {error && <p style={{color: "red"}}>{error}</p>}
      <input placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)}/>
      <input placeholder="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)}/>
      <button type="submit">Log in</button>
    </form>
    )
  }

  return (
    <div>
      <h1>How are you today?</h1>
      <p>{loggedIn? "You are logged in" : "You are not logged in"}</p>
    </div>
  )
}

export default App