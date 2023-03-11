import React from 'react';
import "./App.css";
import Login from "./pages/Login";
import Home from "./pages/home";
import {
	BrowserRouter as Router,
	Switch,
	Route,
	Redirect,
} from "react-router-dom";

function App() {
	return (
		<div className="App">
			<div className="background">
				<Router>
					<Switch>
						<Route exact path="/login">
							<Login />
						</Route>
						<Route exact path="/">
							<Home />
						</Route>
					</Switch>
				</Router>
			</div>
		</div>
	);
}

export default App;
