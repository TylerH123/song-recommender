import React, { useState } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import { Link, useHistory } from "react-router-dom";
import axios from "axios";

const Signup = () => {
  const history = useHistory();
  const [username, setUserName] = useState("");
  const [password, setPassword] = useState();
  const [passwordAgain, setPasswordAgain] = useState();
  async function signUpFunction(e) {
    e.preventDefault();
    console.log("enter");
    let url = `http://localhost:5000`;
    if (password !== passwordAgain) {
      alert("Passwords don't match");
    }
    if (username && password && password === passwordAgain) {
      try {
        console.log("sign up");
        const resp = await axios.post(
          `${url}/register`,
          { username: username, password: password },
          {
            headers: {
              "Content-Type": "application/json",
            },
            mode: "cors",
          }
        );
        console.log(resp.data);
        history.push("/login");
      } catch (err) {
        alert("User already exists");
        console.log(err);
      }
    }
  }
  return (
    <div className="signUpForm">
      <Form className="form rounded p-4 p-sm-3">
        <Form.Group className="mb-3 formGroup" controlId="formBasicName">
          <Form.Label className="label">Username</Form.Label>
          <Form.Control
            className="control"
            type="text"
            placeholder="Enter Username"
            name="username"
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
        <Form.Group className="mb-3 formGroup" controlId="formBasicPassword">
          <Form.Label className="label">Password Again</Form.Label>
          <Form.Control
            className="control"
            type="password"
            placeholder="Password"
            name="password"
            onChange={(e) => setPasswordAgain(e.target.value)}
          />
        </Form.Group>
        <Button
          className="signUpBtn"
          variant="primary"
          type="submit"
          onClick={signUpFunction}
        >
          Sign Up
        </Button>
        <div>
          Have an account?
          <Link to="/login" className="loginHref">
            Login
          </Link>
        </div>
      </Form>
    </div>
  );
};

export default Signup;
