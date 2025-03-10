import { AuthContext } from "../context/AuthContext";
import { useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function ProfileRedirect() {
  const navigate = useNavigate();
  const { user } = useContext(AuthContext);

  //navigate
  useEffect(() => {
    console.log(user?.author_id);
    if (user?.author_id) {
      navigate(`/authors/${user.author_id}`);
    }
  }, [user, navigate]);

  return null;
}
