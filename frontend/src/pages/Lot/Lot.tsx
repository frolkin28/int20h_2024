import { useEffect, useState } from "react";
import { Link as RouterLink } from "react-router-dom";
import axios from "axios";
import { useParams } from "react-router-dom";
import { BetsList, Chat } from "../../components";
import { Lot } from "../../types";
import styles from "./Lot.module.css";
import sharedStyles from "../../App.module.css";
import { transformDate } from "../../utils/dates";

export const LotPage = () => {
  const { lotId } = useParams<{ lotId: string }>();

  const [lot, setLot] = useState<Lot | null>(null);

  useEffect(() => {
    (async () => {
      const res = await axios.get(`${process.env.REACT_APP_BASE_URL}/api/lots/${lotId}`)
      setLot(res.data.data.lot_data)
    })()
  }, [])

  if (!lot) {
    return <h1>Завантаження...</h1>;
  }

  const renderedPictures = lot.pictures.map((picture, index) => {
    return <img key={index} src={picture} width={"250px"} alt="Lot pictures" />;
  });

  return (
    <div className={styles.container}>
      <div className={sharedStyles.card}>
        <h1>{lot.lot_name}</h1>
        <p>{lot.description}</p>
        <p>
          <span className={sharedStyles.bold}>Дата закінчення аукціону: </span> {transformDate(lot.end_date)}
        </p>
        <p>
          <span className={sharedStyles.bold}>Стартова ціна: </span> {lot.start_price}
        </p>
        {lot?.is_author && (
          <div className={styles.container}>
            <RouterLink to={`/lots/edit/${lotId}`}>Редагувати</RouterLink>
          </div>
        )}
        {renderedPictures}
      </div>
      <div className={styles.rightColumn}>
        <BetsList lotId={Number(lotId)} />
        <Chat lotId={Number(lotId)} />
      </div>
    </div>
  );
};
