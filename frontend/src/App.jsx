import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import NavBar from './components/NavBar'
import "./style.css"


createRoot(document.getElementById('root')).render(
  <StrictMode>
    <NavBar />
  </StrictMode>
)
