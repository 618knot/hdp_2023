// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import { Route, Routes } from 'react-router-dom'
import './App.scss'
import Home from './view/home/Home'
import Header from './components/header/Header'

function App() {
  // const [count, setCount] = useState(0)

  return (
    <div className='App'>
      <Header />
      <Routes>
        <Route path='/' element={<Home/>} />
      </Routes>
    </div>
  )
}

export default App
