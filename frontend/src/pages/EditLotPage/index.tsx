import { ChangeEvent, FormEvent, useState } from "react";
import { useParams } from "react-router-dom";

const EditLotPage = () => {
  const initialAuctionState = {
    name: "Sample Auction",
    description: "A description of the auction",
    endDate: "2022-12-31",
  };

  const { lotId } = useParams<{ lotId: string }>();

  const [auction, setAuction] = useState(initialAuctionState);

  const handleInputChange = (
    e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setAuction((prevAuction) => ({
      ...prevAuction,
      [name]: value,
    }));
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    console.log("Auction information submitted:", auction);
  };

  return (
    <div style={styles.container}>
      <h2>Редагування аукціону:</h2>
      <form onSubmit={handleSubmit}>
        <label style={styles.label}>
          Назва:
          <input
            type="text"
            name="name"
            value={auction.name}
            onChange={handleInputChange}
            style={styles.input}
          />
        </label>
        <br />
        <label style={styles.label}>
          Опис:
          <textarea
            name="description"
            value={auction.description}
            onChange={handleInputChange}
            style={styles.textarea}
          />
        </label>
        <br />
        <label style={styles.label}>
          Дата закінчення:
          <input
            type="date"
            name="endDate"
            value={auction.endDate}
            onChange={handleInputChange}
            style={styles.input}
          />
        </label>
        <br />
        <button type="submit" style={styles.button}>
          Зберегти
        </button>
      </form>
    </div>
  );
};

const styles = {
  container: {
    maxWidth: "400px",
    margin: "auto",
    padding: "20px",
    boxShadow: "0 0 10px rgba(0, 0, 0, 0.1)",
    borderRadius: "8px",
    backgroundColor: "#f9f9f9",
  },
  header: {
    textAlign: "center",
    marginBottom: "20px",
    color: "#333",
  },
  form: {
    display: "flex",
    flexDirection: "column",
  },
  label: {
    margin: "10px 0",
    fontSize: "14px",
    color: "#555",
  },
  input: {
    width: "100%",
    padding: "8px",
    fontSize: "14px",
    border: "1px solid #ccc",
    borderRadius: "4px",
  },
  textarea: {
    width: "100%",
    padding: "8px",
    fontSize: "14px",
    border: "1px solid #ccc",
    borderRadius: "4px",
    minHeight: "80px",
  },
  button: {
    backgroundColor: "#3498db",
    color: "#fff",
    padding: "10px",
    fontSize: "16px",
    borderRadius: "4px",
    cursor: "pointer",
  },
};
