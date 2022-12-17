import CommonLayout from "components/layouts/CommonLayout";
import MyCard from "components/MyCard";
import React, { useEffect, useState } from "react";
import { CardGroup, Container } from "react-bootstrap";
import { customAxios } from "util/CustomAxios";

const Posts = () => {
  const [posts, setPosts] = useState([]);

  const getPosts = () => {
    customAxios

      .publicAxios({
        method: `get`,

        url: `/api/v1/posts`,
      })

      .then((response) => {
        console.log(response);

        if (response.status === 200) {
          setPosts(response.data.content);
        }
      })

      .catch((error) => {
        if (error?.response?.data?.detail != null) {
          alert(JSON.stringify(error?.response?.data?.detail));
        } else if (error?.response?.data?.message != null) {
          alert(error.response.data.message);
        } else {
          alert("오류가 발생했습니다. 관리자에게 문의하세요.");
        }
      })

      .finally(() => {});
  };

  useEffect(() => {
    getPosts();
  }, []); // [] 중괄호 안넣으면 무한으로 데이터를 가져옴.

  return (
    <CommonLayout isNavbar={true}>
      <Container className="mt-3">
        <CardGroup className="row-cols-1 row-cols-md-2 row-cols-xl-3 row-cols-xxl-4 card-group">
          {posts.map((post, index) => (
            <MyCard key={index} post={post}></MyCard>
          ))}
        </CardGroup>
      </Container>
    </CommonLayout>
  );
};

export default Posts;
