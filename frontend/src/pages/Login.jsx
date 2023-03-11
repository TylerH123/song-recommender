import React from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import { Link } from "react-router-dom";
const Login = () => {
  return (
    <div className="signUpForm">
      <Form className="form rounded p-4 p-sm-3">
        <Form.Group className="mb-3 formGroup" controlId="formBasicEmail">
          <Form.Label className="label">Username</Form.Label>
          <Form.Control
            className="control"
            type="email"
            placeholder="Enter Username"
          />
        </Form.Group>

        <Form.Group className="mb-3 formGroup" controlId="formBasicPassword">
          <Form.Label className="label">Password</Form.Label>
          <Form.Control
            className="control"
            type="password"
            placeholder="Password"
          />
        </Form.Group>
        <Button className="signUpBtn" variant="primary" type="submit">
          Log In
        </Button>
        <div>
          Don't have an account?
          <Link to="/signup" className="loginHref">
            Sign Up
          </Link>
        </div>
      </Form>
    </div>
  );
};

export default Login;
