import React from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route }
	from 'react-router-dom';
import login from './login';
import home from './home'

function App() {
	return (
		<Router>
			<Routes>
				<Route path='/home' exact element={<home />} />
				<Route path='/login' element={<login />} />
			</Routes>
		</Router>
	);
}

export default App;
