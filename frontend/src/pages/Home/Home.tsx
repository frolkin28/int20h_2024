import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import { LotPreview } from "../../types";
import styles from "./Home.module.css"
import sharedStyles from "../../App.module.css"
import { transformDate } from "../../utils/dates";
import { Button } from "../../components"

export const HomePage = () => {
  const navigate = useNavigate();

  const [lots, setLots] = useState<LotPreview[]>([])
  const [page, setPage] = useState(1)
  const [hasMoreItems, setHasMoreItems] = useState(false)

  useEffect(() => {
    (async () => {
      const res = await axios.get(`${process.env.REACT_APP_BASE_URL}/api/lots/?page=${page}`)
      setLots([...lots, ...res.data.data.lot_data])
      setHasMoreItems(res.data.data.has_more_items)
    })()
  }, [page])

  const renderedLots = lots.map((lot) => (
    <div
      key={lot.lot_id}
      className={`${styles.lotContainer} ${sharedStyles.card}`}
      onClick={() => navigate(`/lots/${lot.lot_id}`)}
    >
      {lot.picture ? <img src={lot.picture} width={"230px"} alt="" /> : null}
      <div>
        <h3>{lot.lot_name}</h3>
        <p className={sharedStyles.withoutMargin}><span className={sharedStyles.bold}>До: </span>{transformDate(lot.end_date)}</p>
        <p className={sharedStyles.withoutMargin}><span className={sharedStyles.bold}>Ціна: </span>{lot.price}₴</p>
      </div>
    </div>
  ));

  return (
    <div>
      <h1>Список лотів</h1>
      <div className={styles.listWrapper}>
        {renderedLots}
      </div>
      {hasMoreItems ? (
        <div className={styles.loadMoreButton}>
          <Button text="Показати більше" onClick={() => setPage(prevState => prevState + 1)} />
        </div>
      ) : null}
    </div>
  );
};
