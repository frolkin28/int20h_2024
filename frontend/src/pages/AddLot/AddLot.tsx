import React, {  useState } from 'react';
import { TextInput } from '../../components';


export const AddLot = () => {
    
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [date, setDate] = useState('');
    const [lot, setLot] = useState('');
    const [amount, setAmount] = useState('');
    const [location, setLocation] = useState ('');

    const handleNameChange = (value: string) => setName(value)
    const handleDescriptionChange = (value: string) => setDescription(value)
    const handleDateChange = (value: string) => setDate(value) 
    const handleLotChange = (value: string) => setLot(value) 
    const handleAmountChange = (value: string) => setAmount(value) 
    const handleLocationChange = (value: string) => setLocation(value) 

    const handleSubmit = async () => {
        if (!name.length) {
          return alert("Введіть назву")
        }
        if (!description.length) {
          return alert("Введіть опис")
        }
        if (!date.length) {
          return alert("Введіть дату")
        }
        if (!lot.length) {
          return alert("Введіть кількість лотів")
        }
        if (!amount.length) {
            return alert("Введіть початкову ціну")
          }
          if (!location.length) {
            return alert("Введіть місто")
          }
    }

        
    return (
        <div className="container">
          <h1>Додати лот</h1>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="name">Назва:</label>
              <TextInput
                id="name"
                value={name}
                onChange={handleNameChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="description">Опис:</label>
              <TextInput
                id="description"
                value={description}
                onChange={handleDescriptionChange}              />
            </div>
            <div className="form-group">
              <label htmlFor="date">Встановити термін аукціону:</label>
              <TextInput
                id="date"
                value={date}
                onChange={handleDateChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="lots">Кількість лотів:</label>
              <TextInput
                id="lots"
                value={lot}
                onChange={handleLotChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="amount">Початкова сума:</label>
              <TextInput
                id="amount"
                value={amount}
                onChange={handleAmountChange}
              />
              <span>грн.</span>
            </div>
            <div className="form-group">
              <label htmlFor="location">Місце знаходження:</label>
              <TextInput
                id="location"
                value={location}
                onChange={handleLocationChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="image">Завантажити зображення:</label>
              <input type="file" id="image" name="image" accept="image/*" />
            </div>
            <button type="submit">Зберегти</button>
          </form>
        </div>
      );

}
export {};