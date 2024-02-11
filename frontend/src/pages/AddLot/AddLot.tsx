import { useContext, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../AuthContext";
import { AddLotForm } from '../../components';

export const AddLotPage = () => {
  const navigate = useNavigate();
  const { isSignedIn } = useContext(AuthContext)

  useEffect(() => {
    if (!isSignedIn) {
      navigate("/sign-in")
    }
  }, [isSignedIn])

  return (
    <>
      <h1>Створення нового лоту</h1>
      <AddLotForm />
    </>
  )
}
