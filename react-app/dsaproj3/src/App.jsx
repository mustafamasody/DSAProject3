import logo from './logo.svg';
import { Routes, Route, BrowserRouter } from 'react-router-dom';
import HomePage from './home';
import './index.css'; 

function App() {
  return (
    <div className="">
      <BrowserRouter>
        <Routes>
            <Route path="/" element={<HomePage />} />
          </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
