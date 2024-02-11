import { useEffect, useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import { BetsList, Chat } from "../../components";
import { Lot } from "../../types"
import styles from "./Lot.module.css"

export const LotPage = () => {
  const { lotId } = useParams<{ lotId: string }>();

  const [lot, setLot] = useState<Lot | null>(null)

  useEffect(() => {
    (async () => {
      try{
        const res = await axios.get(`${process.env.REACT_APP_BASE_URL}/api/lots/${lotId}`)
        setLot(res.data.data.lot_data)
      } catch (error) {
       console.log(error)
      }
    })()
  }, [])

  if (!lot) {
    return <h1>Завантаження...</h1>
  }

  const renderedPictures = lot.pictures.map((picture) => {
    return <img src={picture} width={"250px"} alt="Lot pictures" />
  })

  return (
    <div className={styles.container}>
      <div>
        <h1>{lot.lot_name}</h1>
        <p>{lot.description}</p>
        <p>
          <span>Дата закінчення аукціону: </span> {lot.end_date}
        </p>
        {renderedPictures}
      </div>
      <div className={styles.rightColumn}>
        <BetsList lotId={Number(lotId)} />
        <Chat lotId={Number(lotId)} />
      </div>
    </div>
  );
};
