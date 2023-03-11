import React from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import { Link } from "react-router-dom";

const Signup = () => {
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
        <Form.Group className="mb-3 formGroup" controlId="formBasicPassword">
          <Form.Label className="label">Password Again</Form.Label>
          <Form.Control
            className="control"
            type="password"
            placeholder="Password"
          />
        </Form.Group>
        <Button className="signUpBtn" variant="primary" type="submit">
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
