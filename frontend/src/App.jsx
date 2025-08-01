import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import LoginScreen from './pages/Login'


createRoot(document.getElementById('root')).render(
  <StrictMode>
    <LoginScreen />
  </StrictMode>
)
