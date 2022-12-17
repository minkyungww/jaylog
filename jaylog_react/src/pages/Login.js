import UserInfoLayout from "components/layouts/UserInfoLayout";
import React, { useCallback, useEffect, useRef } from "react";
import { Button, Card, Col, Form, InputGroup, Row } from "react-bootstrap";
import JaylogImg from "assets/img/jaylog.png";
import { Link, useNavigate } from "react-router-dom";
import { useAuthStore } from "stores/RootStore";
import { customAxios } from "util/CustomAxios";

const Login = () => {
    const refs = useRef({
      idElement: null,
      pwElement: null,
      rememberMeElement: null,
    });
  
    const authStore = useAuthStore();
  
    const navigate = useNavigate();
  
    const requestLogin = useCallback(() => {
      if (!validateFields()) {
        return;
      }
  
      const { idElement, pwElement, rememberMeElement } = refs.current;
  
      const loginUser = {
        id: idElement.value,
        password: pwElement.value,
      };
  
      customAxios
        .publicAxios({
          method: `post`,
          url: `/api/v1/sign/in`,
          data: loginUser,
        })
        .then((response) => {
          if (response.status === 200) {
            if (rememberMeElement.checked) {
              localStorage.setItem("rememberId", JSON.stringify(idElement.value));
            } else {
              localStorage.removeItem("rememberId");
            }
            const content = response.data.content;
            localStorage.setItem("accessToken", content.accessToken);
            localStorage.setItem("refreshToken", content.refreshToken);
            authStore.setLoginUserByToken(content.accessToken);
            navigate("/");
          } else {
            alert(response.data.message);
          }
        })
        .catch((error) => {
          if (error?.response?.data?.detail != null) {
            alert(JSON.stringify(error.response.data.detail));
          } else if (error?.response?.data?.message != null) {
            alert(error.response.data.message);
          } else {
            alert("오류가 발생했습니다. 관리자에게 문의하세요.");
          }
        })
        .finally(() => {});
    }, []);
  
    const enterKeyLogin = useCallback((event) => {
      if (event.keyCode === 13) {
        requestLogin();
      }
    }, []);
  
    const validateFields = useCallback(() => {
      if (refs.current.idElement.value === "") {
        alert("아이디를 입력해주세요.");
        refs.current.idElement.focus();
        return false;
      }
  
      if (refs.current.pwElement.value === "") {
        alert("비밀번호를 입력해주세요.");
        refs.current.pwElement.focus();
        return false;
      }
  
      return true;
    }, []);
  
    const setLoginPage = () => {
      refs.current.idElement.focus();
      const rememberId = JSON.parse(localStorage.getItem("rememberId"));
      if (rememberId !== null) {
        refs.current.idElement.value = rememberId;
        refs.current.rememberMeElement.checked = true;
      }
    };
  
    useEffect(() => {
      setLoginPage();
    }, []);
  
    return (
        <UserInfoLayout isNavbar={false}>

        <Card className="shadow-2-strong" style={{ borderRadius: "1rem" }}>
  
          <Card.Body className="p-5 text-center">
  
            <h3 className="mb-3">
  
              <img src={JaylogImg} style={{ height: "100px" }} alt="jaylog"></img>
  
            </h3>
  
            <InputGroup className="mb-3">
  
              <InputGroup.Text id="idAddOn">아이디</InputGroup.Text>
  
              <Form.Control
  
                ref={(el) => (refs.current.idElement = el)}
  
                type="text"
  
                aria-describedby="idAddOn"
  
              />
  
            </InputGroup>
  
            <InputGroup className="mb-3">
  
              <InputGroup.Text id="pwAddOn">비밀번호</InputGroup.Text>
  
              <Form.Control
  
                ref={(el) => (refs.current.pwElement = el)}
  
                type="password"
  
                aria-describedby="pwAddOn"
                onKeyUp={enterKeyLogin}
              />
  
            </InputGroup>
  
            <Form.Group className="d-flex justify-content-start mb-4">
  
              <Form.Check
  
                type="checkbox"
  
                label="아이디 기억하기"
  
                ref={(el) => (refs.current.rememberMeElement = el)}
  
              />
  
            </Form.Group>
  
            <Button
  
              type="button"
  
              className="btn-primary"
  
              style={{ width: "100%" }}
  
              onClick={requestLogin}
  
            >
  
              로그인
  
            </Button>
  
            <hr className="my-4" />
  
            아이디가 없으신가요? <Link to="/join">회원가입</Link>
  
          </Card.Body>
  
        </Card>
  
      </UserInfoLayout>
    );
  };
  
  export default Login;