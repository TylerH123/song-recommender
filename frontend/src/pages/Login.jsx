import React, { useState } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import { Link } from "react-router-dom";
import axios from "axios";
import { useHistory } from "react-router-dom";
const Login = () => {
  const history = useHistory();
  const [username, setUserName] = useState("");
  const [password, setPassword] = useState();
  const [userInfo, setUserInfo] = useState([]);
  async function loginFunction(e) {
    e.preventDefault();
    let url = `http://localhost:5000`;
    try {
      const resp = await axios.post(
        `${url}/login`,
        { username, password },
        {
          headers: {
            "Content-Type": "application/json",
          },
          mode: "cors",
        }
      );
      setUserInfo(resp.data);
      history.push("/weather");
    } catch (err) {
      alert("Could not find user");
      console.log(err);
    }
    // if (username && password && password === passwordAgain) {
    //   try {
    //     console.log("sign up");
    //     const resp = await axios.post(
    //       `${url}/register`,
    //       { username: username, password: password },
    //       {
    //         headers: {
    //           "Content-Type": "application/json",
    //         },
    //         mode: "cors",
    //       }
    //     );
    //     console.log(resp.data);
    //     history.push("/login");
    //   } catch (err) {
    //     alert("User already exists");
    //     console.log(err);
    //   }
    // }
  }
  return (
    <div className="signUpForm">
      <Form className="form rounded p-4 p-sm-3">
        <Form.Group className="mb-3 formGroup" controlId="formBasicName">
          <Form.Label className="label">Username</Form.Label>
          <Form.Control
            className="control"
            type="name"
            placeholder="Enter Username"
            onChange={(e) => setUserName(e.target.value)}
          />
        </Form.Group>

        <Form.Group className="mb-3 formGroup" controlId="formBasicPassword">
          <Form.Label className="label">Password</Form.Label>
          <Form.Control
            className="control"
            type="password"
            placeholder="Password"
            onChange={(e) => setPassword(e.target.value)}
          />
        </Form.Group>
        <Button
          className="signUpBtn"
          variant="primary"
          type="submit"
          onClick={loginFunction}
        >
          Log In
        </Button>
        <div>
          Don't have an account?
          <Link to="/" className="loginHref">
            Sign Up
          </Link>
        </div>
      </Form>
    </div>
  );
};

export default Login;
