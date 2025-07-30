import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import Ping from './pages/teste'


createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Ping />
  </StrictMode>,
)
