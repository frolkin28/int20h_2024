import React, { useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { LotPreview } from "../../types";
import styles from "./Home.module.css"
import sharedStyles from "../../App.module.css"

export const HomePage = () => {
  const navigate = useNavigate();

  const [lots, setLots] = useState<LotPreview[]>([])

  useEffect(() => {
    (async () => {
      const res = await axios.get(`${process.env.REACT_APP_BASE_URL}/api/lots/`)
      setLots(res.data.data.lot_data)
    })()
  }, [])

  const renderedLots = lots.map((lot) => (
    <div className={`${styles.lotContainer} ${sharedStyles.card}`} onClick={() => navigate(`/lots/${lot.lot_id}`)}>
      {lot.picture ? <img src={lot.picture} width={"230px"} alt=""/> : null}
      <div>
        <h3>{lot.lot_name}</h3>
        <p><span>До: </span>{lot.end_date}</p>
      </div>
    </div>
  ))

  return (
    <div>
      <h1>Список лотів</h1>
      <div className={styles.listWrapper}>
        {renderedLots}
      </div>
    </div>
  )
}
