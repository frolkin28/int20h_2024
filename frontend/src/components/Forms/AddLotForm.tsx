import React, { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { FileInput, TextInput, TextArea, Button, DateTimeInput } from "..";
import formStyles from "./Form.module.css"
import axios from "axios";
import { AuthContext } from "../../AuthContext";

export const AddLotForm = () => {
  const navigate = useNavigate();
  const { token } = useContext(AuthContext);

  const [lotName, setLotName] = useState('');
  const [description, setDescription] = useState('');
  const [startPrice, setStartPrice] = useState('');
  const [endDate, setEndDate] = useState('');
  const [images, setImages] = useState<File[]>([]);
  const [isSubmitting, setSubmitting] = useState(false);

  const handleLotNameChange = (value: string) => setLotName(value);
  const handleDescriptionChange = (value: string) => setDescription(value);
  const handleStartPriceChange = (value: string) => setStartPrice(value);
  const handleEndDateChange = (value: string) => setEndDate(value);
  const handleImageChange = (value: File[]) => setImages([...value]);

  const renderedImages = images.map((image) => {
    const url = URL.createObjectURL(image);
    return <img src={url} alt="something" width="250px" />;
  })

  const handleSubmit = async () => {
    setSubmitting(true)

    try {
      if (!lotName.length) {
        return alert("Введіть назву")
      }
      if (!description.length) {
        return alert("Введіть опис")
      }
      if (!endDate.length) {
        return alert("Введіть дату закінчення")
      }
      if (!images.length) {
        return alert("Додайте фотографії")
      }

      const formData = new FormData()
      formData.append("lot_name", lotName)
      formData.append("description", description)
      formData.append("end_date", endDate)
      formData.append("start_price", startPrice)
      images.forEach((image) => formData.append("images", image))

      const res = await axios.post(`${process.env.REACT_APP_BASE_URL}/api/lots/`, formData, {
        headers: {
          'Content-Type': "multipart/form-data",
          'Authorization': `Bearer ${token}`
        },
      })
      navigate(`/lots/${res.data.data.lot_id}`)
    } catch (error: any) {
      alert("Сталася помилка")
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div>
      <form className={formStyles.formContainer}>
        <div className={formStyles.inputBlock}>
          <label className={formStyles.formLabel} htmlFor="lot-name">Назва лоту</label>
          <TextInput
            id="lot-name"
            value={lotName}
            onChange={handleLotNameChange}
          />
        </div>
        <div className={formStyles.inputBlock}>
          <label className={formStyles.formLabel} htmlFor="lot-description">Опис</label>
          <TextArea
            id="lot-description"
            value={description}
            onChange={handleDescriptionChange}
          />
        </div>
        <div className={formStyles.inputBlock}>
          <label className={formStyles.formLabel} htmlFor="start-price">Стартова ціна</label>
          <TextInput
            id="start-price"
            type="number"
            value={startPrice}
            onChange={handleStartPriceChange}
          />
        </div>
        <div className={formStyles.inputBlock}>
          <label className={formStyles.formLabel} htmlFor="end-date">Дата закінчення аукціону</label>
          <DateTimeInput
            id="end-date"
            onChange={handleEndDateChange}
          />
        </div>
        {renderedImages.length ? (
          <div>
            {renderedImages}
          </div>
        ) : null}
        <FileInput multiple={true} onChange={handleImageChange} />
        {images.length ? <Button text="Видалити фото" onClick={() => handleImageChange([])} /> : null}
        <Button text="Створити лот" onClick={handleSubmit} disabled={isSubmitting} />
      </form>
    </div>
  )
}
