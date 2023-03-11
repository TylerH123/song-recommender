import React from 'react';
import './App.css';
import Navbar from './components/Navbar';
import { BrowserRouter as Router, Routes, Route }
	from 'react-router-dom';
import About from './pages/about';
import Blogs from './pages/blogs';
import login from './login';
import Contact from './pages/contact';

function Router() {
	return (
		<Router>
			<Navbar />
			<Routes>
				<Route exact path='/' element={<Home />} />
				<Route path='/about' element={<About />} />
				<Route path='/contact' element={<Contact />} />
				<Route path='/blogs' element={<Blogs />} />
				<Route path='/login' element={<login />} />
			</Routes>
		</Router>
	);
}

export default App;
