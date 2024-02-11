import React, { useEffect } from 'react';
import axios from "axios";

export const HomePage = () => {

  useEffect(() => {
    (async () => {
      const res = await axios.get(`${process.env.REACT_APP_BASE_URL}/api/lots/`)
      console.log(res)
    })()
  }, [])

  return (
    <div>
      <h1>Home</h1>
      <img src={'https://dq5d23gxa9vto.cloudfront.net/2024-02-07%2000.37.28.jpg'}/>
    </div>
  )
}
