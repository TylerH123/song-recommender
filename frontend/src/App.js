import "./App.css";
import Login from "./pages/Login";
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
            <Route exact path="/">
              <Login />
            </Route>
          </Switch>
        </Router>
      </div>
    </div>
  );
}

export default App;
