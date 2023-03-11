import React from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route }
	from 'react-router-dom';
import login from './login';

function App() {
	return (
		<Router>
			<Routes>
				<Route path='/login' element={<login />} />
			</Routes>
		</Router>
	);
}

export default App;
