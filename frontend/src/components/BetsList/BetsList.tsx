import { useContext, useState } from "react";
import { AuthContext } from "../../AuthContext";
import { useAuction } from "../../hooks";
import { BetItem } from "./views/BetItem";
import sharedStyles from "../../App.module.css"

interface BetsListProps {
  lotId: number;
}

export const BetsList = ({ lotId }: BetsListProps) => {
  const { bets, makeBet } = useAuction(lotId);
  const [newBetAmount, setNewBetAmount] = useState("");
  const { isSignedIn } = useContext(AuthContext);

  const handleMakeBet = (e: React.FormEvent) => {
    e.preventDefault();

    if (!isSignedIn) {
      return alert("Необхідно авторизуватись")
    }

    const amount = newBetAmount?.trim()

    if (!amount || amount === "") {
      return alert("Введіть суму")
    }

    const bet = parseFloat(newBetAmount);
    if (bet) {
      makeBet(bet);
      setNewBetAmount("");
    } else {
      alert("Це невалідна сума");
    }
  };

  return (
    <div className={sharedStyles.card}>
      <div>
        <h3 className={sharedStyles.withoutMargin}>Поточні ставки</h3>
      </div>
      <div>
        <ul className={sharedStyles.scrollableContainer}>
          {bets.map((bet) => (
            <BetItem key={bet.id} bet={bet} />
          ))}
        </ul>
        <form onSubmit={handleMakeBet}>
          <label>
            Зробити ставку (грн):
            <input
              type="number"
              value={newBetAmount}
              placeholder="формат 100.00"
              onChange={(e) => setNewBetAmount(e.target.value)}
            />
          </label>

          <button type="submit">
            Підняти
          </button>
        </form>
      </div>
    </div>
  );
};
