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
	import "./App.css";
	import Login from "./pages/Login";
	import {
		createBrowserRouter,
		createRoutesFromElements,
		Route,
		Routes,
		RouterProvider,
	} from "react-router-dom";
	function App() {
		return (
			<div className="App">
				<div className="background">
					<Routes>
						<Route path="/" element={<Login />} />
					</Routes>
				</div>
			</div>
		);
	}

	export default App;
