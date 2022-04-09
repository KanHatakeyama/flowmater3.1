import './router.css';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import React from "react"
import { GraphList } from "./graphs/components/GraphList"
import { Graph } from "./graphs/components/Graph"
import { CreateGraph } from "./graphs/components/CreateGraph"
import Menu from "./Search/components/Menu"
import { PrivateRoute } from "./Login/PrivateRoute"
import { Auth } from "./Login/Auth"

function App() {

  return (
    <div className="App">

      <Menu right width={250} />
      <BrowserRouter>

        <Routes>
          <Route path="/" element={<Auth />} />
          <Route path="/auth" element={<Auth />} />
          <Route path="/private" element={<PrivateRoute><GraphList /></PrivateRoute>} />
          <Route path="/graph/create" element={<PrivateRoute><CreateGraph /></PrivateRoute>} />
          <Route path='/graph/:id' element={<PrivateRoute><Graph /></PrivateRoute>} />
        </Routes>
      </BrowserRouter>
    </div>

  );
}


//            <Route path="/graph" element={<GraphList />} />
export default App;
