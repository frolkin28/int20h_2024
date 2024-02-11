import axios from "axios";
import { ChangeEvent, FormEvent, useContext, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import styles from "./EditLotPage.module.css";
import { DateTimeInput, TextArea, TextInput } from "../../components";
import { AuthContext } from "../../AuthContext";

export const EditLotPage = () => {
  const { lotId } = useParams<{ lotId: string }>();

  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [endDate, setEndDate] = useState("");
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [isAuthor, setisAuthor] = useState(true);
  const { token } = useContext(AuthContext);

  const prepareDate = (value: string) => {
    return new Date(value).toISOString().slice(0, 16);
  };

  const handleDatetimeChange = (e: ChangeEvent<HTMLInputElement>) => {
    setEndDate(e.target.value);
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.get(
          `${process.env.REACT_APP_BASE_URL}/api/lots/${lotId}`
        );
        setName(res.data.data.lot_data.lot_name);
        setDescription(res.data.data.lot_data.description);
        setEndDate(prepareDate(res.data.data.lot_data.end_date));
        setisAuthor(res.data.data.lot_data.is_author);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    navigate(`/lots/${lotId}`);
  }, [isAuthor]);

  if (loading) {
    return <h1>Завантаження...</h1>;
  }
  const postData = async () => {
    setLoading(true);
    try {
      await axios.put(
        `${process.env.REACT_APP_BASE_URL}/api/lots/${lotId}`,
        {
          lot_name: name,
          description: description,
          end_date: endDate,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      navigate(`/lots/${lotId}`);
    } catch (error: any) {
      const errMessage =
        error.response.data.errors?.message ||
        JSON.stringify(error.response.data.errors);
      alert(`Сталася помилка: ${errMessage}`);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (!(name && description && endDate)) {
      alert("Форма не може бути пустою");
    }

    postData();
  };

  return (
    <div className={styles.container}>
      <h2 className={styles.editFormHeader}>Редагування аукціону</h2>
      <form className={styles.editForm} onSubmit={handleSubmit}>
        <div className={styles.inputBlock}>
          <label className={styles.formLabel} htmlFor="lot-name">
            Назва
          </label>
          <TextInput
            id="lot-name"
            value={name}
            onChange={(value) => {
              setName(value);
            }}
          />
        </div>

        <div className={styles.inputBlock}>
          <label className={styles.formLabel} htmlFor="lot-description">
            Опис
          </label>
          <TextArea
            id="lot-description"
            value={description}
            onChange={(value) => {
              setDescription(value);
            }}
          />
        </div>
        <div className={styles.inputBlock}>
          <label className={styles.formLabel} htmlFor="end-date">
            Дата закінчення аукціону
          </label>
          <input
            className={styles.editDTInput}
            type="datetime-local"
            name="editableDatetime"
            value={endDate}
            onChange={handleDatetimeChange}
          />
        </div>
        <button type="submit" className={styles.editSubmitButton}>
          Зберегти
        </button>
      </form>
    </div>
  );
};
